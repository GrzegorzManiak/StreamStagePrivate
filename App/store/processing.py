from events.models import TicketListing

"""
    Queries 'item' price rather than ticket price as I intend
    to use this for subscription purchases also.
"""
def get_item_price(item_id):
    ticket = TicketListing.objects.filter(listing_id = item_id).first()

    if ticket:
        return ticket.price
    
    return None