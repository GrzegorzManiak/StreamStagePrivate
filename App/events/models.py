from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_countries.fields import CountryField
from .validation import validate_event_media, generate_file_media
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
    #picture = models.ImageField("Photograph", upload_to="events", null=True, editable=True)
    media = models.FileField("Media", upload_to=generate_file_media, null=True, editable=True, validators=[validate_event_media])
    description = models.TextField("Media Description", max_length=300, blank=True, null=False)
    content_type = models.TextField("Content Type", editable=False)

    def save(self, *args, **kwargs):
        self.content_type = self.media.path.split("")
        super(EventMedia, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Event Media'
        verbose_name_plural = 'Event Media'

    def __str__(self):
        return self.description[:30]

class EventShowing(models.Model):
    country = CountryField()
    city = models.CharField(max_length=25, blank=True)
    venue = models.CharField(max_length=50, blank=True)
    time = models.DateTimeField()

    class Meta:
        verbose_name = 'Event Showing'
        verbose_name_plural = 'Event Showings'


    def __str__(self):
        return self.location

# when the 'delete event' feature is implemented - all EventMedia objects will need to be deleted by code.
class Event(models.Model):
    event_id = models.CharField(primary_key=True, unique=True, max_length=32) # randomly generated 8 character ID
    title = models.TextField("Title", default="New Event")
    description = models.TextField("Description", blank=True, max_length=3096)
    over_18s = models.BooleanField(default=False)
    # References member, but only "streamers" will be allowed to create an event
    streamer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    categories = models.ManyToManyField(to=Category)
    showings = models.ManyToManyField(to=EventShowing)
    primary_media_idx = models.IntegerField(default=0) # Points to an item in the 'media' field - used as a cover photo 
    media = models.ManyToManyField(to=EventMedia, blank=True)
    contributors = models.ManyToManyField(get_user_model(), related_name="event_broadcasters")

    def get_absolute_url(self):
        return reverse('events.view_event', args=[self.event_id])
    
    def __str__(self):
        return self.title
    
class EventReview(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    rating = models.SmallIntegerField()

    class Meta:
        verbose_name = 'Event Review'
        verbose_name_plural = 'Event Reviews'

    def __str__(self):
        return self.body[:100]