from rest_framework.decorators import api_view
from accounts.com_lib import (
    is_admin, invalid_response, 
    required_data, success_response,
    authenticated
)

from events.models import Event
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
            Q(approved__icontains=data['search'])
        )

    # -- Get the page
    per_page = 10
    total_pages = int(events.count() / per_page)
    processed_events = []
    events = events[page * per_page:page * per_page + per_page]

    # -- Process the events
    for event in events:
        processed_events.append({
            'title': event.title,
            'description': event.description,
            'over_18s': event.over_18s,
            'categories': event.categories,
            'broadcaster': event.broadcaster.handle,
            'broadcaster_id': event.broadcaster.id,
            'created': event.created,
            'updated': event.updated,
        })

    # -- Return the response
    return success_response('Events retrieved successfully', {
        'events': processed_events,
        'page': page,
        'per_page': per_page,
        'total': len(processed_events),
        'pages': total_pages,
    })