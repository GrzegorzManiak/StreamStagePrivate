from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator

from accounts.models import Broadcaster, Member
from datetime import datetime, timedelta
import uuid

# Event/Broadcaster Category Model
class Category(models.Model):
    name = models.CharField("Category Name", max_length=48)
    description = models.TextField("Brief Description", max_length=256)
    splash_photo = models.ImageField(upload_to="events")
    hex_color = models.CharField(max_length=6, default="FFFFFF")

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def get_all_categories(self):
        return Category.objects.all().order_by('name')

class TicketListing(models.Model):
    event = models.ForeignKey(to="events.Event", on_delete=models.CASCADE)
    ticket_detail = models.CharField(max_length=100, blank=True)

    price = models.DecimalField(max_digits=1000, decimal_places=2, validators=[MinValueValidator(0)])

    ticket_type = models.IntegerField(default=0) # streaming ticket ID

    # 0 means no stocking.
    maximum_stock = models.IntegerField(default=0, validators=[MinValueValidator(-1)])
    remaining_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])

# Event Model
class Event(models.Model):
    event_id = models.CharField(primary_key=True, unique=True, max_length=32) # randomly generated 8 character ID
    title = models.TextField("Title", default="New Event")
    description = models.TextField("Description", max_length=3096)
    over_18s = models.BooleanField(default=False)
    broadcaster = models.ForeignKey(Broadcaster, on_delete=models.CASCADE)
    categories = models.ManyToManyField(to=Category)
    primary_media_idx = models.IntegerField(default=0) # Points to an item in the 'media' field - used as a cover photo 
    contributors = models.ManyToManyField(get_user_model(), related_name="event_contributors", blank=True)
    approved = models.BooleanField("Approved", default=False)

    # Event
    
    def get_absolute_url(self):
        return reverse('event_view', args=[self.event_id])
    
    def __str__(self):
        return self.title
    
    def short_description(self):
        return self.description[:250]
    
    # Tickets
    def get_ticket_listings(self):
        return TicketListing.objects.filter(event=self).all()
    
    def has_ticket_listings(self):
        return self.get_ticket_listings().count > 0
    
    # Media

    def get_cover_picture(self):
        media = EventMedia.objects.filter(event=self).all()

        if media.count() == 0:
            return None
        else:
            return media[self.primary_media_idx]

    def get_media(self):
        cover_pic = self.get_cover_picture()
        other_media = EventMedia.objects.filter(event=self).filter(~Q(id=cover_pic.id)).all()
        media = []
        media.append(cover_pic)
        media += other_media

        return media
    
    def get_media_count(self):
        return EventMedia.objects.filter(event=self).all().count()

    # Reviews

    def get_reviews(self):
        return EventReview.objects.filter(event=self).all().order_by('likes')
    
    def get_review_count(self):
        return EventReview.objects.filter(event=self).all().count()
    
    def get_average_rating(self, reviews_in = None):
        avg_rating = 0

        reviews = reviews_in or self.get_reviews()
        count = reviews.count()

        if count > 0:
            for review in reviews:
                avg_rating += review.rating
            
            avg_rating /= count
        
        return round(avg_rating,1)
    
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
    likers = models.ManyToManyField(to=Member)

    class Meta:
        verbose_name = 'Event Review'
        verbose_name_plural = 'Event Reviews'

    def __str__(self):
        return self.body[:100]
    
    def short_review(self):
        self.body = self.body[:50]
        return self
    
    def get_review_body_length(self):
        return len(self.body)

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
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    picture = models.ImageField("Photograph", upload_to="events", null=True, editable=True)
    description = models.TextField("Photograph Description", max_length=300, blank=True, null=False)
    
    class Meta:
        verbose_name = 'Event Media'
        verbose_name_plural = 'Event Media'

    def __str__(self):
        return self.description[:30]


# Event Showing Model
class EventShowing(models.Model):
    showing_id = (models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False))
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    country = CountryField()
    city = models.CharField(max_length=25, blank=True)
    venue = models.CharField(max_length=50, blank=True)
    time = models.DateTimeField()

    class Meta:
        verbose_name = 'Event Showing'
        verbose_name_plural = 'Event Showings'

    def __str__(self):
        return self.time.strftime("%H:%M %d-%m-%Y")
