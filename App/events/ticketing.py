from .models import TicketListing

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