from rest_framework.decorators import api_view
from accounts.com_lib import (
    is_admin, invalid_response, 
    required_data, success_response,
    authenticated
)

from events.models import Event, EventShowing
from accounts.models import Broadcaster
from django.db.models import Q

sorts = ['updated', 'created', 'title', 'description', 'over_18s', 'categories', 'approved']
orders = ['asc', 'desc']



@api_view(['GET', 'POST'])
@is_admin()
@required_data(['page', 'sort', 'order', 'search'])
def events(request, data):

    # -- Make sure all the data is valid
    try: 
        page = int(data['page'])
        if page < 0: return invalid_response('Page must be greater than 0')
    except ValueError: return invalid_response('Page must be an integer')

    if data['sort'] not in sorts: return invalid_response('Invalid sort')
    if data['order'] not in orders: return invalid_response('Invalid order')

    # -- Get the categorys
    filter = {}

    # -- Sort
    match data['sort']:
        case 'updated': sort = 'updated'
        case 'created': sort = 'created'
        case 'title': sort = 'title'
        case 'description': sort = 'description'
        case 'over_18s': sort = 'over_18s'
        case 'categories': sort = 'categories'
        case 'approved': sort = 'approved'

    # -- Order
    if data['order'] == 'desc': sort = '-' + sort
    else: sort = sort

    # -- Get the events
    events = Event.objects.filter(**filter).order_by(sort)

    # -- Search
    if len(data['search']) > 3:
        events = events.filter(
            Q(title__icontains=data['search']) |
            Q(description__icontains=data['search']) |
            Q(over_18s__icontains=data['search']) |
            Q(categories__icontains=data['search']) |
            Q(approved__icontains=data['search']) |
            Q(broadcaster__handle__icontains=data['search'])
        )

    # -- Get the page
    per_page = 5
    total_pages = int(events.count() / per_page)
    processed_events = []
    events = events[page * per_page:page * per_page + per_page]

    # -- Process the events
    for event in events:
        processed_events.append({
            'title': event.title,
            'description': event.description,
            'over_18s': event.over_18s,
            'categories': [{
                'id': category.id,
                'name': category.name,
            } for category in event.categories.all()],
            'broadcaster': {
                'id': event.broadcaster.id,
                'handle': event.broadcaster.handle,
            },
            'created': event.created,
            'updated': event.updated,
            'contributors': [{
                'id': contributor.id,
                'handle': contributor.username,
            } for contributor in event.contributors.all()],
            'approved': event.approved,
            'id': event.event_id,
            'showings': [{
                'id': showing.showing_id,
            } for showing in EventShowing.objects.filter(event=event).all()],
        })

    # -- Return the response
    return success_response('Events retrieved successfully', {
        'events': processed_events,
        'page': page,
        'per_page': per_page,
        'total': len(processed_events),
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
    return success_response('Event retrieved successfully', {
        'title': event.title,
        'description': event.description,
        'over_18s': event.over_18s,
        'categories': event.categories,
        'broadcaster': event.broadcaster.handle,
        'broadcaster_id': event.broadcaster.id,
        'created': event.created,
        'updated': event.updated,
    })



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
