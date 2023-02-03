from django.shortcuts import render
from .models import Event, EventShowing

def view_event(request, event_id):
    event = Event.objects.filter(event_id=event_id).first()

    return render(request, 'event.html', {'event':event})