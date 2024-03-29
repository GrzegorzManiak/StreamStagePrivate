from django.contrib import admin
from .models import TicketListing, Event, EventMedia, Category, EventShowing, EventReview, EventTrailer

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [ 'event_id', 'title', 'description', 'over_18s', 'broadcaster', 'approved']
    list_editable = [ 'title', 'description', 'over_18s', 'broadcaster', 'approved']
    list_display_links = []
@admin.register(TicketListing)
class TicketListing(admin.ModelAdmin):
    list_display = [ 'event', 'price', 'ticket_detail', 'ticket_type', 'maximum_stock', 'remaining_stock' ]
    list_editable = [ 'price', 'ticket_detail', 'ticket_type', 'maximum_stock', 'remaining_stock']
    list_display_links = []

@admin.register(EventMedia)
class EventMediaAdmin(admin.ModelAdmin):
    list_display = [ 'event', 'picture', 'description' ]
    list_editable = [ 'picture', 'description' ]
    link_display_links = []

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'description', 'splash_photo', 'hex_color' ]
    list_editable = [ 'description', 'splash_photo', 'hex_color' ]
    list_displaylinks = []

@admin.register(EventShowing)
class EventShowingAdmin(admin.ModelAdmin):
    list_display = [ 'showing_id', 'event', 'country', 'city', 'venue', 'time', 'max_duration' ]
    list_editable = [ 'event', 'country', 'city', 'venue', 'time', 'max_duration']
    list_displaylinks = []

@admin.register(EventReview)
class EventReviewAdmin(admin.ModelAdmin):
    list_display = [ 'review_id', 'author', 'event', 'title', 'body', 'likes', 'rating' ]
    list_editable = [ 'author', 'title', 'body', 'likes', 'rating' ]
    list_display_links = []

@admin.register(EventTrailer)
class EventTrailerAdmin(admin.ModelAdmin):
    list_display = [ 'event', 'videofile', 'description' ]
    list_editable = [ 'videofile', 'description' ]
    list_display_links = []
