from django.contrib import admin
from .models import Event, EventMedia, Category, EventShowing

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
class ShowingAdmin(admin.ModelAdmin):
    list_display = [ 'location', 'time' ]
