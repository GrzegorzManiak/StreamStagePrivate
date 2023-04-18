from events.models import Event
from accounts.models import Member
from store.models import TicketListing
from .models import Purchase, PurchaseItem
from StreamStage.models import Statistics
import uuid
    
def create_purchase(
    purchase_id: uuid.uuid4,
    stripe_intent: dict,
    purchaser: Member, 
    billing_data, 
    ticket_listing: TicketListing, 
    total_mult: float = 1
):
    stripe_id = stripe_intent["id"]
    payment_id = stripe_intent["payment_method"]

    purchase = Purchase.objects.create(
        stripe_id = stripe_id,
        payment_id = payment_id,
        purchase_id = purchase_id,
        purchaser = purchaser,
        billingName = billing_data["billingName"],
        billingAddress1 = billing_data["billingAddress1"],
        billingCity = billing_data["billingCity"],
        billingPostcode = billing_data["billingPostcode"],
        billingCountry = billing_data["billingCountry"],
        total_multiplier = total_mult
    )

    item = PurchaseItem.objects.create(
        purchase = purchase,
        item_name = ticket_listing.ticket_detail,
        price = ticket_listing.price
    )

    Statistics.log('payment', 'gross', (ticket_listing.price * total_mult))
    Statistics.log('tickets', 'gross', (ticket_listing.price * total_mult))
    Statistics.log('tickets', 'count', 1)

    purchase.save()
    item.save()


