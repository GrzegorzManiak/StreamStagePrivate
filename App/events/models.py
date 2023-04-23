import base64
import io

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from PIL import Image

from django.db import models
from django.db.models import Q, Avg, Max, Min

from django.contrib.auth import get_user_model
from django.urls import reverse
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator
from StreamStage.templatetags.tags import cross_app_reverse

from StreamStage.settings import MEDIA_URL
from datetime import datetime, timedelta, time
from django.core.files import File
from PIL import Image
import uuid
import base64

# Event/Broadcaster Category Model
class Category(models.Model):
    name = models.CharField("Category Name", max_length=48)
    description = models.TextField("Brief Description", max_length=256)
    splash_photo = models.ImageField(upload_to="events", blank=True, null=True)
    hex_color = models.CharField(max_length=6, default="FFFFFF")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def get_all_categories(self):
        return Category.objects.all().order_by('name')
    


    def add_pic_from_base64(self, base64_data: str):
        """
            Sets the category photo from a base64 
            string, and saves it to the media folder
        """
        try:
            img_tmp = NamedTemporaryFile(delete=True)
            image_data = base64.b64decode(base64_data.split(',')[1])
            image = Image.open(io.BytesIO(image_data))

            # -- Compress the image
            image = image.save(img_tmp, 'webp', quality=75)

            # -- Save the image to the media folder
            img_tmp.write(image_data)
            img_tmp.flush()

            img = File(img_tmp, name=f'categories/{uuid.uuid4()}.webp')
            self.splash_photo = img

            self.save()
            return True

        except Exception as e:
            print(e)
            return False


    def get_splash_photo(self):
        """
            Returns the splash photo for the category
            or a placeholder image if no photo is set
        """
        if self.splash_photo is not None or self.splash_photo != "":
            return f'/{MEDIA_URL}{self.splash_photo}'
        else: return "/static/img/placeholder.png"


    def serialize(self):
        """
            Returns a serialized version of the category
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.hex_color,
            'created': self.created,
            'updated': self.updated,
            'image': self.get_splash_photo()
        }


class TicketListing(models.Model):
    listing_id = models.UUIDField(default=uuid.uuid4)
    event = models.ForeignKey(to="events.Event", on_delete=models.CASCADE)
    ticket_detail = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=1000, decimal_places=2, validators=[MinValueValidator(0)])
    
    # seat = models.CharField(max_length=25, blank=True)
    
    ticket_type = models.IntegerField(default=0) # streaming ticket ID

    # If this is an in-person ticket, a showing must be specified.
    showing = models.ForeignKey(to="events.EventShowing", null=True, on_delete=models.CASCADE)

    # 0 means no stocking.
    maximum_stock = models.IntegerField(default=0, validators=[MinValueValidator(-1)])
    remaining_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def serialize(self):
        if self.ticket_type == 0: # streaming
            return {
                'id': self.listing_id,
                'detail': self.ticket_detail,
                'price': self.price,
                'stock': self.remaining_stock,
                'ticket_type': self.ticket_type
            }
        else:
            return {
                'id': self.listing_id,
                'detail': self.ticket_detail,
                'price': self.price,
                'stock': self.remaining_stock,
                'ticket_type': self.ticket_type,
                'showing_id': self.showing.showing_id
            }

# Event Model
class Event(models.Model):
    event_id = models.CharField(primary_key=True, unique=True, max_length=32) # randomly generated 8 character ID
    title = models.TextField("Title", default="New Event")
    description = models.TextField("Description", max_length=3096)
    over_18s = models.BooleanField(default=False)
    broadcaster = models.ForeignKey(to="accounts.Broadcaster", on_delete=models.CASCADE)
    categories = models.ManyToManyField(to=Category)
    primary_media_idx = models.IntegerField(default=0) # Points to an item in the 'media' field - used as a cover photo 
    contributors = models.ManyToManyField(get_user_model(), related_name="event_contributors", blank=True)
    approved = models.BooleanField("Approved", default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # Event
    
    def get_absolute_url(self):
        return cross_app_reverse('events', 'event_view', kwargs=[self.event_id])
    
    def __str__(self):
        return self.title
    
    # Tickets
    def get_ticket_listings(self):
        return TicketListing.objects.filter(event=self).all()
    
    def get_streaming_ticket_listings(self):
        return TicketListing.objects.filter(event=self,ticket_type=0).all()
    
    def has_ticket_listings(self):
        return self.get_ticket_listings().count()
    
    def get_max_price_ticket(self):
        tickets = self.get_ticket_listings().all()
        max_price = 0
        for ticket in tickets:
            if ticket.price > max_price:
                max_price = ticket.price
        return TicketListing.objects.filter(price=max_price).first()
    
    def get_min_ticket_price(self):
        tickets = self.get_ticket_listings().all()
        min_price = 9999
        for ticket in tickets:
            if ticket.price < min_price:
                min_price = ticket.price
        return TicketListing.objects.filter(price=min_price).first()

    # Media

    def get_cover_picture(self):
        media = EventMedia.objects.filter(event=self).all()

        if media.count() == 0:
            return None
        else:
            return media[self.primary_media_idx]

    def get_media(self):
        cover_pic = self.get_cover_picture()
        other_media = EventMedia.objects.filter(event=self).filter(~Q(media_id=cover_pic.media_id)).all()
        media = []
        media.append(cover_pic)
        media += other_media

        return media
    
    def get_media_count(self):
        return EventMedia.objects.filter(event=self).all().count()
    
    # Trailer 
    def get_trailer(self): 
        return EventTrailer.objects.filter(event=self).all()
    
    # Reviews

    def get_reviews(self):
        return EventReview.objects.filter(event=self).all().order_by('likes')
    
    def get_medium_reviews(self):
        reviews = EventReview.objects.filter(event=self).all().order_by('likes')
        for review in reviews:
            review.body = review.body[:250]
        return reviews 
       
    def get_short_reviews(self):
        reviews = EventReview.objects.filter(event=self).all().order_by('likes')
        for review in reviews:
            review.body = review.body[:50]
        return reviews
    
    def get_review_count(self):
        return EventReview.objects.filter(event=self).all().count()
    
    def get_average_rating(self, reviews_in = None):
        # avg_rating = 0

        # reviews = reviews_in or self.get_reviews()
        # count = reviews.count()

        # if count > 0:
        #     for review in reviews:
        #         avg_rating += review.rating
            
        #     avg_rating /= count
        
        # return round(avg_rating,1)
        return EventReview.objects.filter(event=self).aggregate(Avg("rating"))["rating__avg"] or 0
    
    # Get top review based on likes
    def get_top_review(self, reviews_in = None):
        reviews = reviews_in or self.get_reviews()

        top_review = None
        likes = 0
        for review in reviews:
            if review.likes >= likes:
                likes = review.likes
                top_review = review
        return top_review
    
    # Showings

    def get_showings(self):
        return EventShowing.objects.filter(event=self).all().order_by('time')

    # def get_showings(self):
    #     showings = EventShowing.objects.filter(event=self).all().order_by('time')
    #     for showing in showings:
    #         showing.time = showing.time(tz = showing.time.tzinfo)
    #     return showings

    def get_next_showing(self):
        return self.get_showings().first()

    def get_last_showing(self):
        return self.get_showings().last()
    
    def get_num_upcoming_showings(self):
        showings = []
        for showing in self.get_showings():
            if showing.time + timedelta(hours=1) >= datetime.now(tz = showing.time.tzinfo):
                showings.append(showing)
        return len(showings)
    
    def get_showings_count(self):
        return EventShowing.objects.filter(event=self).all().count()
    
    def is_event_live(self):
        showings = []
        for showing in self.get_showings():
            time_left = datetime.now(tz = showing.time.tzinfo) - showing.time
            if time_left < timedelta(minutes=showing.max_duration) and time_left.total_seconds() > 0:
                showings.append(showing)
        if len(showings) > 0:        
            return True 

    def get_category_names(self):
        names = []

        for category in self.categories.values():
            names.append(category.name)

        return names


    def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'over_18s': self.over_18s,
            'categories': [{
                'id': category.id,
                'name': category.name,
            } for category in self.categories.all()],
            'broadcaster': {
                'id': self.broadcaster.id,
                'handle': self.broadcaster.handle,
            },
            'created': self.created,
            'updated': self.updated,
            'contributors': [{
                'id': contributor.id,
                'handle': contributor.username,
            } for contributor in self.contributors.all()],
            'approved': self.approved,
            'id': self.event_id,
            'showings': [{
                'id': showing.showing_id,
            } for showing in EventShowing.objects.filter(event=self).all()],
        }
    
    def is_authorized(self, user):
        return (
            user.is_staff
            or  self.broadcaster.streamer == user
            or  self.broadcaster.contributors.filter(id=user.id).exists()
        )



# Event Review Model
class EventReview(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(get_user_model(), related_name="Author", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField("Review Title", max_length=50)
    body = models.TextField("Review Body", max_length=500)
    created = models.DateTimeField("Created", auto_now_add=True)
    updated = models.DateTimeField("Updated", auto_now=True)
    likes = models.IntegerField("Review Likes", default=0)
    rating = models.SmallIntegerField("Event Rating", default=10, validators=[MinValueValidator(0), MaxValueValidator(10)])
    likers = models.ManyToManyField(to="accounts.Member")

    class Meta:
        verbose_name = 'Event Review'
        verbose_name_plural = 'Event Reviews'

    def __str__(self):
        return self.title
    
    def get_review_body_length(self):
        return len(self.body)

    def get_rating(self):
        return self.rating

    def get_review_likes(self):
        return EventReview.objects.filter(event=self).filter(review_id=self.review_id).count()
    
    def toggle_like(self, member):
        if member in self.likers.all():
            self.likers.remove(member)
        else:
            self.likers.add(member)
        self.likes = self.likers.count()
        self.save()

    def user_liked(self, member):
        return member in self.likers.all()
    
    def get_likers_list(self):
        list = []
        for liker in self.likers.all():
            list.append(liker.id)
        return list


# Event Media Model
class EventMedia(models.Model):
    media_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    picture = models.ImageField("Photograph", upload_to="events", null=True, editable=True)
    description = models.TextField("Photograph Description", max_length=300, blank=True, null=False)
    
    class Meta:
        verbose_name = 'Event Media'
        verbose_name_plural = 'Event Media'

    def __str__(self):
        return self.description[:30]

    def load_from_base64(self, base64_data: str):
        """
            Saves a picture file to the media folder
            and then associates this event media object
            with that file. 
        """
        try:
            img_tmp = NamedTemporaryFile()
            image_data = base64.b64decode(base64_data.split(',')[1])
            image = Image.open(io.BytesIO(image_data))

            # -- Compress the image
            image = image.save(img_tmp, 'webp', quality=75)

            # -- Save the image to the media folder
            img_tmp.write(image_data)
            img_tmp.flush()

            self.picture = File(img_tmp, name=f'{uuid.uuid4()}.webp')

            self.save()

            return True
        except Exception as e:
            print("ERROR")
            print(e)
            return False
# Event Trailer Model
class EventTrailer(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    videofile= models.FileField(upload_to='videos/', verbose_name="")
    description = models.TextField("Trailer Description", max_length=300, blank=True, null=False)
    
    class Meta:
        verbose_name = 'Event Trailer'
        verbose_name_plural = 'Event Trailers'

    def __str__(self):
        return self.description[:30]
    
# Event Showing Model
class EventShowing(models.Model):
    showing_id = (models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False))
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    country = CountryField("Country")
    city = models.CharField("City", max_length=25, blank=True)
    venue = models.CharField("Venue", max_length=50, blank=True)
    time = models.DateTimeField()
    max_duration = models.SmallIntegerField("Max Duration (in minutes)")

    class Meta:
        verbose_name = 'Event Showing'
        verbose_name_plural = 'Event Showings'

    def get_ticket_listings(self):
        return TicketListing.objects.filter(showing=self).all()

    def __str__(self):
        return self.time.strftime("%H:%M %d-%m-%Y")
