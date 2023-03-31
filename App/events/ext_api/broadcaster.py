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

from accounts.models import Broadcaster
from django.db.models import Q

sorts = ['updated', 'created', 'handle', 'over_18', 'approved']
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
            Q(approved__icontains=data['search'])
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
            'updated': broadcaster.updated
        })
