from django.db import models
from StreamStage.templatetags.tags import cross_app_reverse
from events.models import EventShowing, TicketListing
from orders.models import PurchaseItem
from StreamStage.identifiers import new_ticket_id
import uuid

class FlexibleTicket(models.Model):
    ticket_id = models.CharField(primary_key=True, unique=True, max_length=20, default=new_ticket_id)
    purchase_id = models.UUIDField(editable=False, null=False, default=uuid.uuid4)
    item = models.ForeignKey(PurchaseItem, on_delete=models.SET_NULL, null=True)
    
    listing = models.ForeignKey(TicketListing, null=True, on_delete=models.DO_NOTHING) # if event is deleted - keep ticket
    
    purchased_date = models.DateTimeField(auto_now_add=True)
    
    # if this is a streaming ticket - field is null until member chooses a showing to watch
    # if a live ticket - then the field should point to the showing that the member has purchased a ticket for. 
    showing = models.ForeignKey(EventShowing, null=True, on_delete=models.DO_NOTHING)

    #ticket_price = models.DecimalField("Price", decimal_places=2, max_digits=10)

    def getOwner(self):
        return self.purchase.purchaser
    
    def serialize(self):
        return {
            "ticket_id": self.ticket_id,
            "purchase_id": self.purchase_id,
            "listing": self.listing.serialize(),
            "purchased_date": self.purchased_date.strftime("%Y-%m-%d %H:%M:%S"),
            "showing": self.showing.serialize() if self.showing else None,
            "streaming_ticket": self.listing.ticket_type == 0,
            "event_url": cross_app_reverse('events', 'event_view', {
                'event_id': self.listing.event.event_id
            }),
        }