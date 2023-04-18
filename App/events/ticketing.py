from .models import TicketListing

class TicketType:
    Streaming = 0
    LiveTicket = 1

    Types = [ Streaming, LiveTicket ]

def create_ticket_listing(event, ticket_type, price, stock = -1, details = None, showing = None):
    # Add default ticket listings
    if ticket_type == TicketType.Streaming:
        listing = TicketListing(
            event = event,
            ticket_detail = "Streaming Ticket" if not details else details,
            ticket_type = ticket_type,
            price = price
        )
    elif ticket_type == TicketType.LiveTicket:


        listing = TicketListing(
            event = event,
            ticket_detail = "In-Person Ticket"if not details else details,
            ticket_type = ticket_type,
            price = price,
            maximum_stock = stock,
            remaining_stock = stock,
            showing = showing
        )
    else:
        print(f"Ticketing Error: Tried to create ticket of unknown type ({ticket_type})")
        return None
    
    if details is not None:
        listing.ticket_details = details
    
    listing.save()

    return listing
