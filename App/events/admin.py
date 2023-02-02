from django.contrib import admin
from .models import Event, EventMedia, Category, Showing

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = [ 'event_id', 'event_title', 'description', 'streamer' ]

class EventMediaAdmin(admin.ModelAdmin):
    list_display = [ 'picture', 'description' ]

class CategoryAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'description', 'splash_photo' ]

class ShowingAdmin(admin.ModelAdmin):
    list_display = [ 'location', 'time' ]

admin.site.register(Event, EventAdmin)
admin.site.register(Showing, ShowingAdmin)
admin.site.register(EventMedia, EventMediaAdmin)
admin.site.register(Category, CategoryAdmin)