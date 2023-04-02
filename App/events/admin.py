from django.contrib import admin
from .models import TicketListing, Event, EventMedia, Category, EventShowing, EventReview

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [ 'event_id', 'title', 'description', 'over_18s', 'broadcaster', 'approved']
    list_editable = [ 'title', 'description', 'over_18s', 'broadcaster', 'approved']
    list_display_links = []
    filter_horizontal = ['contributors']

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
    list_display = [ 'name', 'description', 'splash_photo' ]
    list_editable = [ 'description', 'splash_photo' ]
    list_displaylinks = []

@admin.register(EventShowing)
class EventShowingAdmin(admin.ModelAdmin):
    list_display = [ 'showing_id', 'event', 'country', 'city', 'venue', 'time' ]
    list_editable = [ 'event', 'country', 'city', 'venue', 'time' ]
    list_displaylinks = []

@admin.register(EventReview)
class EventReviewAdmin(admin.ModelAdmin):
    list_display = [ 'review_id', 'author', 'event', 'title', 'body', 'likes', 'rating' ]
    list_editable = [ 'author', 'title', 'body', 'likes', 'rating' ]
    list_display_links = []

