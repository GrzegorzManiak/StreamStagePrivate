from events.models import Event
from accounts.models import Member
from store.models import FlexibleTicket
from models import Purchase, PurchaseItem

def create_flexible_ticket(purchaser: Member, event: Event):
    ticket = FlexibleTicket(
        purchaser = purchaser,
        event = event,
        # ticket_price = event.stream_price
    )
    
def create_purchase(purchaser: Member, billing_data, ticket: FlexibleTicket):
    purchase = Purchase(
        purchaser = purchaser,
        billingName = billing_data["billingName"],
        billingAddress1 = billing_data["billingAddress1"],
        billingCity = billing_data["billingCity"],
        billingPostcode = billing_data["billingPostcode"],
        billingCountry = billing_data["billingCountry"],
        total_multiplier = 1
    )

    # todo: calculate premium discounts here

    item = PurchaseItem(
        purchase = purchase,
        item_name = "Streaming Ticket",
        price = ticket.ticket_price
    )