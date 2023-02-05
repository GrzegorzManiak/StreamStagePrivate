from django.contrib import admin
from .models import Event, EventMedia, Category, EventShowing, EventReview

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [ 'event_id', 'title', 'description', 'streamer' ]

@admin.register(EventMedia)
class EventMediaAdmin(admin.ModelAdmin):
    list_display = [ 'picture', 'description' ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'description', 'splash_photo' ]

@admin.register(EventShowing)
class EventShowingAdmin(admin.ModelAdmin):
    list_display = [ 'location', 'time' ]

@admin.register(EventReview)
class EventReviewAdmin(admin.ModelAdmin):
    list_display = ['review_id', 'author', 'review_title', 'review_text']

