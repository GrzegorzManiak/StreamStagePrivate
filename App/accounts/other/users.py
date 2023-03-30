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
@required_data(['page', 'sort', 'order', 'position', 'search'])
def users(request, data):
    """
        This view returns all users in the database in a formatted list.
        Some data is truncated to save performance.
    """

    # -- Make sure all the data is valid
    try: 
        page = int(data['page'])
        if page < 0: return invalid_response('Page must be greater than 0')
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
        case 'created': sort = 'date_joined'
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
    if len(data['search']) > 3:
        users = users.filter(
            Q(username__icontains=data['search']) | 
            Q(email__icontains=data['search']) |
            Q(country__icontains=data['search']) |
            Q(first_name__icontains=data['search']) |
            Q(last_name__icontains=data['search']) |
            Q(description__icontains=data['search'])
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
        'users': processed_users,
        'page': page,
        'per_page': per_page,
        'total': len(processed_users),
        'pages': total_pages,
    })



@api_view(['GET'])
@is_admin()
@required_data(['id'])
def get_user(request, data):
    """
        This view returns a single user in the database in a formatted list.
        Some data is truncated to save performance.
    """
    # -- Get the user
    user = Member.objects.filter(id=data['id']).first()
    if user is None: return invalid_response('User does not exist')

    # -- Format the data
    return success_response('Successfully retrieved user', {
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
        'description': user.description,
        'id': user.id,
    })