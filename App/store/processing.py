from orders.models import PurchaseItem
from orders.processing import create_purchase
from store.models import FlexibleTicket
from accounts.models import Member
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

def create_ticket(ticket_listing: TicketListing, purchase_item: PurchaseItem):
    ticket = FlexibleTicket(
        item = purchase_item,
        listing = ticket_listing,
        showing = None
    )
    
    return ticket

"""
    Gets called when a payment intent is checked, and it is
    successful.
"""
def on_intent_success(cust_payment_intent):
    billing_data = {
        "billingName": "",
        "billingAddress1": "",
        "billingCity": "",
        "billingPostcode": "",
        "billingCountry": "",
    }

    item_ids = cust_payment_intent["items"]
    items = reverse_items(item_ids)

    for item in items:        
        # currently all items are TicketListings, but may not always be.
        if item is TicketListing:
            purchase_item = create_purchase(cust_payment_intent.user, billing_data, item)

            create_ticket(item, purchase_item)


def reverse_items(item_ids):
    return [ listing for listing in TicketListing.objects.filter(listing_id__in=item_ids)]