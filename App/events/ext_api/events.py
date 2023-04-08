from rest_framework.decorators import api_view
from accounts.com_lib import (
    is_admin, invalid_response, 
    required_data, success_response,
    paginate
)

from events.models import Event
from accounts.models import Broadcaster


@api_view(['GET', 'POST'])
@is_admin()
@paginate(
    page_size=10,
    search_fields=['title', 'description', 'over_18s', 'categories__name', 
                   'categories__description', 'approved', 'broadcaster__handle'],
    order_fields=['updated', 'created', 'title', 'description', 'over_18s', 'categories', 'approved'],
    model=Event
)
def events(request, models, total_pages, page):
    """
        Gets all events
    """

    # -- Return the response
    return success_response('Events retrieved successfully', {
        'events': [event.serialize() for event in models],
        'page': page,
        'per_page': 10,
        'total': len(models),
        'pages': total_pages,
    })



@api_view(['GET', 'POST'])
@is_admin()
@required_data(['id'])
def get_event(request, data):
    # -- Get the event
    try: event = Event.objects.get(id=data['id'])
    except Event.DoesNotExist: return invalid_response('Event does not exist')

    # -- Return the response
    return success_response('Event retrieved successfully', event.serialize())



@api_view(['DELETE'])
@is_admin()
@required_data(['id'])
def delete_event(request, data):
    # -- Get the event
    try: event = Event.objects.get(id=data['id'])
    except Event.DoesNotExist: return invalid_response('Event does not exist')

    # -- Delete the event
    event.delete()

    # -- Return the response
    return success_response('Event deleted successfully', {})



@api_view(['POST'])
@is_admin()
@required_data(['id', 'title', 'description', 'over_18s', 'categories', 'broadcaster_id'])
def update_event(request, data):
    # -- Get the event
    try: event = Event.objects.get(id=data['id'])
    except Event.DoesNotExist: return invalid_response('Event does not exist')

    # -- Get the broadcaster
    try: broadcaster = Broadcaster.objects.get(id=data['broadcaster_id'])
    except Broadcaster.DoesNotExist: return invalid_response('Broadcaster does not exist')

    # -- Update the event
    event.title = data['title']
    event.description = data['description']
    event.over_18s = data['over_18s']
    event.categories = data['categories']
    event.broadcaster = broadcaster
    event.save()

    # -- Return the response
    return success_response('Event updated successfully', {})
