import datetime
from StreamStage.templatetags.tags import cross_app_reverse

from accounts.models import Broadcaster
from .api_auth import can_edit_event
from accounts.com_lib import authenticated, invalid_response, error_response, required_data, success_response
from rest_framework.decorators import api_view
from .models import TicketListing, EventShowing, Event, EventMedia

from .ticketing import create_ticket_listing, TicketType

# TICKET LISTING APIs

@api_view(['POST'])
@authenticated()
@required_data(['event_id'])
def get_ticket_listings(request, data):
    """
        This view is used to get ticket listings
        for a particular event
    """

    event = Event.objects.filter(event_id=data['event_id']).first()

    if not event:
        return error_response('Event with given ID not found.')

    listings = TicketListing.objects.filter(
        event=event
    )

    encoded_listings = []
    
    for listing in listings:
        encoded_listings.append(listing.serialize())

    return success_response('Listings retrieved successfully', {
        'listings': encoded_listings
    })

@api_view(['POST'])
@required_data(['event_id', 'ticket_type', 'detail', 'price', 'stock'])
@can_edit_event()
def add_ticket_listing(request, event, data):
    ticket_type = data['ticket_type']
    price = data['price']
    stock = data['stock']
    detail = data['detail']

    if ticket_type not in TicketType.Types:
        return error_response('Invalid ticket type.')
    
    if price < 0:
        return error_response('Invalid price.')
    
    showing = None

    if ticket_type is TicketType.LiveTicket:
        showing_id = request.data.get('showing_id')

        showing = EventShowing.objects.filter(showing_id=showing_id).first()

        if showing is None:
            return error_response('Must specify valid showing to create a live ticket.')
    
    listing = create_ticket_listing(event, ticket_type, price, stock, detail, showing)

    if not listing:
        return error_response('Unknown error.')

    encoded_listing = {
        'id': listing.listing_id,
        'detail': listing.ticket_detail,
        'price': listing.price,
        'stock': listing.remaining_stock,
        'ticket_type': listing.ticket_type,
        'showing_id': listing.showing.showing_id if listing.showing else None
    }

    return success_response('Successfully added listing', {
        'listing': encoded_listing
    })

@api_view(['POST'])
@authenticated()
@required_data(['event_id', 'listing_id'])
def del_ticket_listing(request, data):
    if not request.user.is_streamer:
        return error_response('Permission denied: you are not a streamer.')

    event = Event.objects.filter(event_id=data['event_id']).first()

    if not event:
        return error_response('Event with given ID not found.')
    
    # TODO: contributors check
    if request.user != event.broadcaster.streamer:
        return error_response('Permission denied: you do not have permissions to edit provided event.')
    
    listing = TicketListing.objects.filter(listing_id = data['listing_id']).first()

    if listing is None or listing.event != event:
        return error_response('Permission denied: invalid listing id.')
    
    listing.delete()

    return success_response('Successfully deleted listing')



# SHOWING APIs

@api_view(['POST'])
@authenticated()
@required_data(['event_id'])
def get_showings(request, data):
    """
        This api is used to get showings for a particular event
    """
    
    event = Event.objects.filter(event_id=data['event_id']).first()

    if not event:
        return error_response('Event with given ID not found.')

    showings = EventShowing.objects.filter(
        event=event
    )

    encoded_showings = []
    
    for showing in showings:
        encoded_showings.append({
            'showing_id': showing.showing_id,
            'country': showing.country.name,
            'city': showing.city,
            'venue': showing.venue,
            'time': (showing.time.strftime("%d %B, %Y - %H:%M")),
            'max_duration': showing.max_duration
        })

    return success_response('Event showings retrieved successfully', {
        'showings': encoded_showings
    })

@api_view(['POST'])
@authenticated()
@required_data(['event_id', 'time', 'venue', 'city', 'country'])
def add_showing(request, data):
    if not request.user.is_streamer:
        return error_response('Permission denied: you are not a streamer.')

    event = Event.objects.filter(event_id=data['event_id']).first()

    if not event:
        return error_response('Event with given ID not found.')
    
    # TODO: contributors check
    if request.user != event.broadcaster.streamer:
        return error_response('Permission denied: you do not have permissions to edit provided event.')

    time = data['time']
    venue = data['venue']
    city = data['city']
    country = data['country']
    
    showing = EventShowing(
        event = event,
        time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M'),
        venue = venue,
        city = city,
        country = country,
        max_duration = 120
    )
    showing.save()

    encoded_showing = {
        'showing_id': showing.showing_id,
        'country': showing.country.name,
        'city': showing.city,
        'venue': showing.venue,
        'time': showing.time.strftime("%d %B, %Y - %H:%M"),
        'max_duration': showing.max_duration
    }

    return success_response('Successfully added showing', {
        'showing': encoded_showing
    })

@api_view(['POST'])
@authenticated()
@required_data(['event_id', 'showing_id'])
def del_showing(request, data):
    if not request.user.is_streamer:
        return error_response('Permission denied: you are not a streamer.')

    event = Event.objects.filter(event_id=data['event_id']).first()

    if not event:
        return error_response('Event with given ID not found.')
    
    # TODO: contributors check
    if request.user != event.broadcaster.streamer:
        return error_response('Permission denied: you do not have permissions to edit provided event.')
    
    showing = EventShowing.objects.filter(showing_id = data['showing_id']).first()

    if showing is None or showing.event != event:
        return error_response('Permission denied: invalid showing ID.')
    
    showing.delete()

    return success_response('Successfully deleted event showing.')





# MEDIA APIs
@api_view(['POST'])
@authenticated()
@required_data(['event_id'])
def get_media(request, data):
    event = Event.objects.filter(event_id=data['event_id']).first()

    if not event:
        return error_response('Event with given ID not found.')

    evt_media = EventMedia.objects.filter(
        event=event
    )

    encoded_media = []
    
    for media in evt_media:
        encoded_media.append({
            'media_id': media.media_id,
            'description': media.description,
            'picture': media.picture.url
        })

    return success_response('Event media retrieved successfully.', {
        'media': encoded_media
    })

@api_view(['POST'])
@authenticated()
@required_data(['event_id', 'picture', 'description'])
def add_media(request, data):
    if not request.user.is_streamer:
        return error_response('Permission denied: you are not a streamer.')

    event = Event.objects.filter(event_id=data['event_id']).first()

    if not event:
        return error_response('Event with given ID not found.')
    
    # TODO: contributors check
    if request.user != event.broadcaster.streamer:
        return error_response('Permission denied: you do not have permissions to edit provided event.')

    description = data['description']
    picture = data['picture']
    
    media = EventMedia(
        event = event,
        description = description
    )

    if not media.load_from_base64(picture):
        return error_response('Unknown error occured while adding event media.')
    
    encoded_media = {
        'media_id': media.media_id,
        'description': media.description,
        'picture': media.picture.url
    }

    return success_response('Successfully added event media.', {
        'media': encoded_media
    })

@api_view(['POST'])
@authenticated()
@required_data(['event_id', 'media_id'])
def del_media(request, data):
    if not request.user.is_streamer:
        return error_response('Permission denied: you are not a streamer.')

    event = Event.objects.filter(event_id=data['event_id']).first()

    if not event:
        return error_response('Event with given ID not found.')
    
    # TODO: contributors check
    if request.user != event.broadcaster.streamer:
        return error_response('Permission denied: you do not have permissions to edit provided event.')
    
    media = EventMedia.objects.filter(media_id = data['media_id']).first()

    if media is None or media.event != event:
        return error_response('Permission denied: invalid media ID.')
    
    media.delete()

    return success_response('Successfully deleted event media.')



@api_view(['GET', 'POST'])
@required_data(['broadcaster_id', 'sort', 'order', 'page'])
def get_bc_events(request, data):
    """
        This view is used to get the events
        for a broadcaster.
    """
    
    # -- Pagination
    try: 
        page = int(data['page'])
        if page < 0: return invalid_response('Page must be greater than 0')
    except ValueError: return invalid_response('Page must be an integer')

    valid_sorts = ['rating']
    if data['sort'] not in valid_sorts: return invalid_response('Invalid sort')

    valid_orders = ['asc', 'desc']
    if data['order'] not in valid_orders: return invalid_response('Invalid order')

    

    per_page = 5
    sort = '-' + data['sort'] if data['order'] == 'desc' else data['sort']

    # -- Get the broadcaster
    try: broadcaster = Broadcaster.objects.get(id=data['broadcaster_id'])
    except Broadcaster.DoesNotExist: return invalid_response('Broadcast er does not exist')

    # -- Get the reviews
    events = Event.objects.filter(
        broadcaster=broadcaster
    )#.order_by(sort)

    total_pages = int(len(events) / per_page)
    serialized_events = []
    events = events[page * per_page: (page + 1) * per_page]
    for event in events:
        serialized_reviews = []

        for review in event.get_reviews():
            serialized_reviews.append({
                'id': review.review_id,
                'event': review.event.event_id,
                'event_name': review.event.title,
                'rating': review.rating,
                'body': review.body,
                'title': review.title,
                'created': review.created,
                'likes': review.likes,
                'username': review.author.username,
            })
        
        serialized_events.append({
            'event_id': event.event_id,
            'rating': event.get_average_rating(),
            'categories': event.get_category_names(),
            'cover_pic': event.get_cover_picture() or '',
            'url': cross_app_reverse('events', 'event_view', { "event_id": event.event_id }),
            'description': event.description,
            'title': event.title,
            'reviews': serialized_reviews,
        })

    # -- Return the reviews
    return success_response('Events retrieved successfully', {
        'events': serialized_events,
        'page': page,
        'per_page': per_page,
        'total': len(serialized_events),
        'pages': total_pages,
    })


# @api_view(['POST'])
# @required_data(['event_id', 'title', 'description', 'categories', 'primary_media_idx'])
# @can_edit_event()
# def update_event_details(request, event:Event, data):
    
#     event.title = data['title']
#     event.description = data['description']
#     event.primary_media_idx = data['primary_media_idx']
#     event.over_18s = data['over_18s']

#     #categories

#     return success_response('Successfully updated event details.')

# @api_view(['GET'])
# @required_data(['event_id'])
# @can_edit_event()
# def get_event_details(request, event:Event, data):
#     """
#         Returns the event with the given id.
#     """
    
#     return success_response('Successfully retrieved event', {
#     })