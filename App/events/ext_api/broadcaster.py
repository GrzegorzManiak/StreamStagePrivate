"""
    This file contains the API endpoints for the broadcaster model.
    The reason that this is here not in the accounts app is because
    the broadcaster model is used in the events app and not touched
    by the accounts app.
"""

from rest_framework.decorators import api_view
from accounts.com_lib import (
    is_admin, invalid_response, 
    required_data, success_response,
    authenticated
)

from accounts.models import Broadcaster, Member
from django.db.models import Q

sorts = ['updated', 'created', 'handle', 'name', 'biography', 'over_18', 'approved']
orders = ['asc', 'desc']

@api_view(['GET', 'POST'])
@is_admin()
@required_data(['page', 'sort', 'order', 'search'])
def broadcasters(request, data):
    # -- Make sure all the data is valid
    try: 
        page = int(data['page'])
        if page < 0: return invalid_response('Page must be greater than 0')
    except ValueError: return invalid_response('Page must be an integer')

    if data['sort'] not in sorts: return invalid_response('Invalid sort')
    if data['order'] not in orders: return invalid_response('Invalid order')


    # -- Get the broadcasters
    filter = {}

    # -- Sort
    match data['sort']:
        case 'updated': sort = 'updated'
        case 'created': sort = 'created'
        case 'handle': sort = 'handle'
        case 'over_18': sort = 'over_18'
        case 'approved': sort = 'approved'
        case 'name': sort = 'name'
        case 'biography': sort = 'biography'

    # -- Order
    if data['order'] == 'desc': sort = '-' + sort
    else: sort = sort

    # -- Get the broadcasters
    broadcasters = Broadcaster.objects.filter(**filter).order_by(sort)

    # -- Search
    if len(data['search']) > 3:
        broadcasters = broadcasters.filter(
            Q(handle__icontains=data['search']) |
            Q(over_18__icontains=data['search']) |
            Q(approved__icontains=data['search']) |
            Q(biography__icontains=data['search']) |
            Q(name__icontains=data['search']) |
            Q(biography__icontains=data['search'])
        )

    # -- Paginate
    per_page = 10
    total_pages = int(broadcasters.count() / per_page)
    processed = []
    broadcasters = broadcasters[page * per_page:page * per_page + per_page]

    # -- Process the broadcasters
    for broadcaster in broadcasters:
        processed.append({
            'id': broadcaster.id,
            'handle': broadcaster.handle,
            'over_18': broadcaster.over_18,
            'approved': broadcaster.approved,
            'created': broadcaster.created,
            'updated': broadcaster.updated,
            'name': broadcaster.name,
            'biography': broadcaster.biography,
            'streamer': broadcaster.streamer.id,
            'profile_picture': broadcaster.get_picture('profile_pic'),
            'profile_banner': broadcaster.get_picture('banner')
        })

    # -- Return the response
    return success_response('Successfully retrieved broadcasters', {
        'broadcasters': processed,
        'page': page,
        'per_page': per_page,
        'total': len(processed),
        'pages': total_pages
    })



@api_view(['GET'])
@is_admin()
@required_data(['id'])
def get_broadcaster(request, data):
    """
        Simply returns the broadcaster with the given id.
    """
    try:broadcaster = Broadcaster.objects.get(id=data['id'])
    except Broadcaster.DoesNotExist:
        return invalid_response('Broadcaster does not exist')

    return success_response('Successfully retrieved broadcaster', {
        'id': broadcaster.id,
        'handle': broadcaster.handle,
        'over_18': broadcaster.over_18,
        'approved': broadcaster.approved,
        'created': broadcaster.created,
        'updated': broadcaster.updated,
        'name': broadcaster.name,
        'biography': broadcaster.biography,
        'streamer': broadcaster.streamer.id,
        'profile_picture': broadcaster.get_picture('profile_pic'),
        'profile_banner': broadcaster.get_picture('banner')
    })



@api_view(['POST'])
@is_admin()
@required_data(['id', 'handle', 'over_18', 'approved', 'name', 'biography', 'owner'])
def update_broadcaster(request, data):
    """
        Updates the broadcaster with the given id.
    """
    try:broadcaster = Broadcaster.objects.get(id=data['id'])
    except Broadcaster.DoesNotExist:
        return invalid_response('Broadcaster does not exist')
    
    # -- try and find the streamer (either by id or handle)
    if data['owner'].count('@') > 0:
        username  = data['owner'].replace('@', '').lower()

        try:streamer = Member.objects.get(username=username)
        except Member.DoesNotExist:
            return invalid_response('Streamer does not exist')
        
    else:
        try:streamer = Member.objects.get(id=data['owner'])
        except Member.DoesNotExist:
            return invalid_response('Streamer does not exist')
        
    # -- Make sure the streamer is a streamer
    if not streamer.is_streamer:
        return invalid_response('Selected user is not a streamer')

    broadcaster.handle = data['handle']
    broadcaster.over_18 = data['over_18']
    broadcaster.approved = data['approved']
    broadcaster.name = data['name']
    broadcaster.biography = data['biography']
    broadcaster.streamer = streamer
    broadcaster.save()

    return success_response('Successfully updated broadcaster', {
        'id': broadcaster.id,
        'handle': broadcaster.handle,
        'over_18': broadcaster.over_18,
        'approved': broadcaster.approved,
        'created': broadcaster.created,
        'updated': broadcaster.updated,
        'name': broadcaster.name,
        'biography': broadcaster.biography,
        'streamer': broadcaster.streamer.id,
        'profile_picture': broadcaster.get_picture('profile_pic'),
        'profile_banner': broadcaster.get_picture('banner')
    })



@api_view(['DELETE'])
@is_admin()
@required_data(['id'])
def delete_broadcaster(request, data):
    """
        Deletes the broadcaster with the given id.
    """
    try:broadcaster = Broadcaster.objects.get(id=data['id'])
    except Broadcaster.DoesNotExist:
        return invalid_response('Broadcaster does not exist')

    broadcaster.delete()
    return success_response('Successfully deleted broadcaster', {})