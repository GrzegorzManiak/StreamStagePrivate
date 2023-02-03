from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid

class Category(models.Model):
    name = models.CharField("Category Name", max_length=48)
    description = models.TextField("Brief Description", max_length=256)
    splash_photo = models.ImageField(upload_to="events")

    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class EventMedia(models.Model):
    picture = models.ImageField("Photograph", upload_to="events", null=True)
    description = models.TextField("Photograph Description", max_length=300, blank=True, null=False)
    
    class Meta:
        verbose_name_plural = 'Event Media'

    def __str__(self):
        return self.description[:30]

class EventShowing(models.Model):
    location = models.CharField(blank=True, max_length=64)
    time = models.DateField()

    def __str__(self):
        return self.location

# when the 'delete event' feature is implemented - all EventMedia objects will need to be
# deleted by code.
class Event(models.Model):
    event_id = models.CharField(primary_key=True, unique=True, max_length=8) # randomly generated 8 character ID
    title = models.TextField("Title", default="New Event")
    description = models.TextField("Description", blank=True, max_length=3096)
    # References member, but only "streamers" will be allowed to have an event
    streamer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    categories = models.ManyToManyField(to=Category)
    showings = models.ManyToManyField(to=EventShowing)
    media = models.ManyToManyField(to=EventMedia, blank=True)

    def get_absolute_url(self):
        return reverse('events.view_event', args=[self.event_id])
    
    def __str__(self):
        return self.event_title
    