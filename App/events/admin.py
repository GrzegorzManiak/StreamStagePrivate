from django.contrib import admin
from .models import Event, EventMedia, Category, EventShowing, EventReview

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = [ 'event_id', 'event_title', 'description', 'streamer' ]

class EventMediaAdmin(admin.ModelAdmin):
    list_display = [ 'picture', 'description' ]

class CategoryAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'description', 'splash_photo' ]

class EventShowingAdmin(admin.ModelAdmin):
    list_display = [ 'location', 'time' ]

class EventReviewAdmin(admin.ModelAdmin):
    list_display = ['review_id', 'author', 'review_title', 'review_text']

admin.site.register(Event, EventAdmin)
admin.site.register(EventShowing, EventShowingAdmin)
admin.site.register(EventMedia, EventMediaAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(EventReview, EventReviewAdmin)
