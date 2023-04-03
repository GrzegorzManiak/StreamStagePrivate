from events.models import Event
from accounts.models import Member
from store.models import TicketListing
from .models import Purchase, PurchaseItem
    
def create_purchase(purchaser: Member, billing_data, ticket_listing: TicketListing, total_mult: float = 1):
    purchase = Purchase(
        purchaser = purchaser,
        billingName = billing_data["billingName"],
        billingAddress1 = billing_data["billingAddress1"],
        billingCity = billing_data["billingCity"],
        billingPostcode = billing_data["billingPostcode"],
        billingCountry = billing_data["billingCountry"],
        total_multiplier = total_mult
    )

    item = PurchaseItem(
        purchase = purchase,
        item_name = ticket_listing.ticket_detail,
        price = ticket_listing.price
    )


