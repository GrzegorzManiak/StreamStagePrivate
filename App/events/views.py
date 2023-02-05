from django.shortcuts import render
from .models import Event, EventShowing

# could be done with a class view, running the queries in
# get_context_objects, but currently I see no significant benefit
# in doing so.
def view_event(request, event_id):
    event = Event.objects.filter(event_id=event_id).first()
    
    primary_media_idx = event.primary_media_idx
    
    media = event.media.all()

    if media.count() == 0:
        cover_pic = None
    else:
        cover_pic = media[primary_media_idx]

    return render(request, 'event.html', {'event':event, 'cover_pic': cover_pic})