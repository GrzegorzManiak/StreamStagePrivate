from accounts.com_lib import authenticated, invalid_response, error_response, required_data, success_response
from rest_framework.decorators import api_view
from .models import TicketListing, EventShowing, Event

from .ticketing import create_ticket_listing, TicketType

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
        encoded_listings.append({
            'id': listing.listing_id,
            'detail': listing.ticket_detail,
            'price': listing.price,
            'stock': listing.remaining_stock
        })

    return success_response('Listings retrieved successfully', {
        'listings': encoded_listings
    })

@api_view(['POST'])
@authenticated()
@required_data(['event_id', 'ticket_type', 'detail', 'price', 'stock'])
def add_ticket_listing(request, data):
    if not request.user.is_streamer:
        return error_response('Permission denied: you are not a streamer.')

    event = Event.objects.filter(event_id=data['event_id']).first()

    if not event:
        return error_response('Event with given ID not found.')
    
    # TODO: contributors check
    if request.user != event.broadcaster.streamer:
        return error_response('Permission denied: you do not have permissions to edit provided event.')

    ticket_type = data['ticket_type']
    price = data['price']
    stock = data['stock']
    detail = data['detail']

    if ticket_type not in TicketType.Types:
        return error_response('Invalid ticket type.')
    
    if price < 0:
        return error_response('Invalid price.')
    
    listing = create_ticket_listing(event, ticket_type, price, stock, detail)

    if not listing:
        return error_response('Unknown error.')

    encoded_listing = {
        'id': listing.listing_id,
        'detail': listing.ticket_detail,
        'price': listing.price,
        'stock': listing.remaining_stock
    }

    # -- Return the reviews
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

    # -- Return the reviews
    return success_response('Successfully deleted listing')





# @api_view(['POST'])
# @authenticated()
# @required_data(['event_id'])
# def get_showings(request, data):
#     """
#         This view is used to get ticket listings
#         for a particular event
#     """

#     event = Event.objects.filter(event_id=data['event_id']).first()

#     if not event:
#         return error_response('Event with given ID not found.')

#     showings = EventShowing.objects.filter(
#         event=event
#     )

#     encoded_showings = []
    
#     for showing in showings:
#         encoded_showings.append({
#             'id': showing.listing_id,
#             'detail': listing.ticket_detail,
#             'price': listing.price,
#             'stock': listing.remaining_stock
#         })

#     return success_response('Listings retrieved successfully', {
#         'listings': encoded_listings
#     })
