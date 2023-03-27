from accounts.com_lib import authenticated, invalid_response, error_response, required_data, success_response
from rest_framework.decorators import api_view
from .models import TicketListing, Event

class TicketType:
    Streaming = 0
    LiveTicket = 1

def add_ticket_listing(event, ticket_type, price, stock = -1, details = None):
    # Add default ticket listings
    if ticket_type == TicketType.Streaming:
        listing = TicketListing(
            event = event,
            ticket_details = "Streaming Ticket",
            ticket_type = ticket_type,
            price = price
        )
    elif ticket_type == TicketType.LiveTicket:
        listing = TicketListing(
            event = event,
            ticket_details = "In-Person Ticket",
            ticket_type = ticket_type,
            price = price,
            maximum_stock = stock,
            remaining_stock = stock
        )
    else:
        print(f"Ticketing Error: Tried to create ticket of unknown type ({ticket_type})")
        return
    
    if details is not None:
        listing.ticket_details = details
    
    listing.save()

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

    # -- Get the reviews
    listings = TicketListing.objects.filter(
        event=event
    )

    encoded_listings = []
    
    for listing in listings:
        encoded_listings.append({
            'id': listing.id,
            'detail': listing.ticket_detail,
            'price': listing.price,
            'stock': listing.remaining_stock
        })

    # -- Return the reviews
    return success_response('Reviews retrieved successfully', {
        'listings': encoded_listings
    })
