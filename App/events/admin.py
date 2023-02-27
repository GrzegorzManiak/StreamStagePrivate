from django.contrib import admin
from .models import Event, EventMedia, Category, EventShowing, EventReview

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [ 'event_id', 'title', 'description', 'over_18s', 'broadcaster', 'media', 'approved']
    list_editable = [ 'title', 'description', 'over_18s', 'broadcaster', 'media', 'approved']
    list_display_links = []
    filter_horizontal = ['contributors']

@admin.register(EventMedia)
class EventMediaAdmin(admin.ModelAdmin):
    list_display = [ 'picture', 'description' ]
    # list_editable = [ 'picture', 'description' ]
    # link_display_links = []

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'description', 'splash_photo' ]
    # list_editable = [ 'name', 'description', 'splash_photo' ]
    # list_displaylinks = []

@admin.register(EventShowing)
class EventShowingAdmin(admin.ModelAdmin):
    list_display = [ 'country', 'city', 'venue', 'time' ]

@admin.register(EventReview)
class EventReviewAdmin(admin.ModelAdmin):
    list_display = ['review_id', 'author', 'title', 'body', 'likes', 'rating']
    list_editable = [ 'title', 'body', 'likes', 'rating']
    list_display_links = []

