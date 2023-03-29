from rest_framework.decorators import api_view
from accounts.com_lib import is_admin, invalid_response, required_data, success_response
from events.models import EventReview

from accounts.models import Member
from django.db.models import Q


positions = ['all', 'user', 'admin', 'streamer']
sorts = ['updated', 'created', 'username', 'email', 'position', 'country']
orders = ['asc', 'desc']

@api_view(['GET', 'POST'])
@is_admin()
@required_data(['page', 'sort', 'order', 'position', 'q'])
def users(request, data):
    """
        This view returns all users in the database in a formatted list.
        Some data is truncated to save performance.
    """

    # -- Make sure all the data is valid
    try: page = int(data['page'])
    except ValueError: return invalid_response('Page must be an integer')

    if data['sort'] not in sorts: return invalid_response('Invalid sort')
    if data['order'] not in orders: return invalid_response('Invalid order')
    if data['position'] not in positions: return invalid_response('Invalid position')

    # -- Get the users
    filter = {}

    
    # -- Position
    match data['position']:
        case 'user': filter['is_staff'] = False
        case 'admin': filter['is_staff'] = True
        case 'streamer': filter['is_streamer'] = True
        case 'all': pass

    # -- Sort
    match data['sort']:
        case 'updated': sort = 'last_login'
        case 'created': sort = 'created'
        case 'username': sort = 'username'
        case 'email': sort = 'email'
        case 'position': sort = 'is_staff'
        case 'country': sort = 'country'

    # -- Order
    if data['order'] == 'desc': sort = '-' + sort
    else: sort = sort

    # -- Get the users  
    users = Member.objects.filter(**filter).order_by(sort)

    # -- Search
    if len(data['q']) > 3:
        users = users.filter(
            Q(username__icontains=data['q']) | 
            Q(email__icontains=data['q']) |
            Q(country__icontains=data['q']) |
            Q(first_name__icontains=data['q']) |
            Q(last_name__icontains=data['q']) |
            Q(description__icontains=data['q'])
        )

    # -- Handle pagination
    per_page = 10
    total_pages = int(len(users) / per_page)
    processed_users = []
    users = users[page * per_page: (page + 1) * per_page]

    # -- Format the data
    for user in users:
        processed_users.append({
            'username': user.username,
            'cased_username': user.cased_username,

            'email': user.email,
            'streamer': user.is_streamer,
            'over_18': user.over_18,
            'is_staff': user.is_staff,

            'profile_picture': user.get_profile_pic(),
            'profile_banner': user.get_profile_banner(),

            'updated': user.last_login,
            'created': user.date_joined,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'description': user.description[:100] + '...' if len(user.description) > 100 else user.description,
            'id': user.id,
        })

    # -- Format the data
    return success_response('Successfully retrieved users', {
        'reviews': processed_users,
        'page': page,
        'per_page': per_page,
        'total': len(processed_users),
        'pages': total_pages,
    })