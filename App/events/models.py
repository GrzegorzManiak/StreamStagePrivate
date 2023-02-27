from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator 

from accounts.models import Broadcaster

import uuid

class Category(models.Model):
    name = models.CharField("Category Name", max_length=48)
    description = models.TextField("Brief Description", max_length=256)
    splash_photo = models.ImageField(upload_to="events")

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class EventMedia(models.Model):
    picture = models.ImageField("Photograph", upload_to="events", null=True, editable=True)
    description = models.TextField("Photograph Description", max_length=300, blank=True, null=False)
    
    class Meta:
        verbose_name = 'Event Media'
        verbose_name_plural = 'Event Media'

    def __str__(self):
        return self.description[:30]

class EventShowing(models.Model):
    showing_id = (models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False))
    country = CountryField()
    city = models.CharField(max_length=25, blank=True)
    venue = models.CharField(max_length=50, blank=True)
    time = models.DateTimeField()

    class Meta:
        verbose_name = 'Event Showing'
        verbose_name_plural = 'Event Showings'


    def __str__(self):
        return self.venue

# when the 'delete event' feature is implemented - all EventMedia objects will need to be deleted by code.
class Event(models.Model):
    event_id = models.CharField(primary_key=True, unique=True, max_length=32) # randomly generated 8 character ID
    title = models.TextField("Title", default="New Event")
    description = models.TextField("Description", max_length=3096)
    over_18s = models.BooleanField(default=False)
    # Which broadcaster this event is going to be attributed to.
    broadcaster = models.ForeignKey(Broadcaster, on_delete=models.CASCADE)
    # References member, but only "streamers" will be allowed to create an event
    #streamer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    categories = models.ManyToManyField(to=Category)
    showings = models.ManyToManyField(to=EventShowing, blank=True, related_name="showings")
    primary_media_idx = models.IntegerField(default=0) # Points to an item in the 'media' field - used as a cover photo 
    media = models.ManyToManyField(to=EventMedia, blank=True)
    contributors = models.ManyToManyField(get_user_model(), related_name="event_broadcasters", blank=True)
    approved = models.BooleanField("Approved", default=False)

    def get_absolute_url(self):
        return reverse('event_view', args=[self.event_id])
    
    def __str__(self):
        return self.title
    
    def short_description(self):
        return self.description[:200]
    
    def get_average_rating(self, reviews_in = None):
        avg_rating = 0

        reviews = reviews_in or self.get_reviews()
        count = reviews.count()

        if count > 0:
            for review in reviews:
                avg_rating += review.rating
            
            avg_rating /= count
        
        return round(avg_rating,1)

    def get_cover_picture(self):
        media = self.media.all()

        if media.count() == 0:
            return None
        else:
            return media[self.primary_media_idx]

    def get_reviews(self):
        return EventReview.objects.filter(event=self).all()
    
    def get_top_review(self, reviews_in = None):
        reviews = reviews_in or self.get_reviews()

        top_review = None
        rating = 0
        for review in reviews:
            if review.rating > rating:
                rating = review.rating
                top_review = review
        return top_review
    
class EventReview(models.Model):

    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField("Review Title", max_length=50)
    body = models.TextField("Review Body", max_length=500)
    created = models.DateTimeField("Created", auto_now_add=True)
    updated = models.DateTimeField("Updated", auto_now=True)
    likes = models.IntegerField("Review Likes", default=0)
    rating = models.SmallIntegerField("Event Rating", default=10, validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        verbose_name = 'Event Review'
        verbose_name_plural = 'Event Reviews'

    def __str__(self):
        return self.body[:100]
