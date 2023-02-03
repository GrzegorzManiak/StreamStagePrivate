from django.shortcuts import render
from .models import Event, EventShowing

# could be done with a class view, running the queries in
# get_context_objects, but currently I see no significant benefit
# in doing so.
def view_event(request, event_id):
    event = Event.objects.filter(event_id=event_id).first()
    
    return render(request, 'event.html', {'event':event})