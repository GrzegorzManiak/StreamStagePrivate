from orders.models import Purchase, PurchaseItem
from orders.processing import create_purchase
from store.models import FlexibleTicket
from accounts.models import Member
from events.models import TicketListing
import uuid

"""
    Queries 'item' price rather than ticket price as I intend
    to use this for subscription purchases also.
"""
def get_item_price(item_id):
    ticket = TicketListing.objects.filter(listing_id = item_id).first()

    if ticket:
        return ticket.price
    
    return None

def create_ticket(
    purchase_id: uuid.UUID,
    ticket_listing: TicketListing, 
    purchase_item: PurchaseItem
):
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
    purchase_id = uuid.uuid4()

    for item in items:        
        # currently all items are TicketListings, but may not always be.
        if isinstance(item, TicketListing):
            purchase_item = create_purchase(
                purchase_id,
                cust_payment_intent['stripe_intent'],
                cust_payment_intent["user"], 
                billing_data, item
            )

            create_ticket(
                purchase_id,
                item, 
                purchase_item
            )

    return purchase_id

def reverse_items(item_ids):
    return [ listing for listing in TicketListing.objects.filter(listing_id__in=item_ids)]


def on_subscription_success(cust_payment_intent):
    billing_data = {
        "billingName": "",
        "billingAddress1": "",
        "billingCity": "",
        "billingPostcode": "",
        "billingCountry": "",
    }

    purchase_id = uuid.uuid4()
    stripe_intent = cust_payment_intent["stripe_intent"]
    stripe_id = stripe_intent["id"]

    purchase = Purchase.objects.create(
        stripe_id = stripe_id,
        payment_id = cust_payment_intent['payment_method'],
        purchase_id = purchase_id,
        purchaser = cust_payment_intent["user"],
        billingName = billing_data["billingName"],
        billingAddress1 = billing_data["billingAddress1"],
        billingCity = billing_data["billingCity"],
        billingPostcode = billing_data["billingPostcode"],
        billingCountry = billing_data["billingCountry"],
        total_multiplier = 1,
    )

    # -- Set the details on the user
    user = cust_payment_intent["user"]
    start_date = stripe_intent['current_period_start']
    end_date = stripe_intent['current_period_end']
    plan = stripe_intent['plan']['interval']

    user.has_subscription = True
    user.subscription_id = stripe_id
    user.subscription_start = int(start_date)
    user.subscription_end = int(end_date)
    user.subscription_status = plan
    
    purchase.save()
    user.save()
    return purchase_id