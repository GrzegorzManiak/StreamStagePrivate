from django.contrib import admin
from .models import *

@admin.register(EventApplication)
class EventAppAdmin(admin.ModelAdmin):
    list_display = [ 'applicant', 'event', 'submitted', 'status' ]
    
@admin.register(StreamerApplication)
class StreamerAppAdmin(admin.ModelAdmin):
    list_display = [ 'applicant', 'event', 'submitted', 'status' ]
    
@admin.register(BroadcasterApplication)
class BroadcasterAppAdmin(admin.ModelAdmin):
    list_display = [ 'applicant', 'broadcaster', 'submitted', 'status' ]
    