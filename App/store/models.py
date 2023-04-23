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
        self.showing = self.listing.showing 
        
        return {
            "ticket_id": self.ticket_id,
            "purchase_id": self.purchase_id,
            "listing": self.listing.serialize(),
            "purchased_date": self.purchased_date.strftime("%Y-%m-%d %H:%M:%S"),
            "showing": self.showing.serialize() if self.showing else None,
            "price": self.listing.price,
            "streaming_ticket": self.listing.ticket_type == 0,
            "event": {
                "url": cross_app_reverse('events', 'event_view', {
                    'event_id': self.listing.event.event_id
                }),
                "broadcaster_name": self.listing.event.broadcaster.handle,
                "title": self.listing.event.title,
                "event_id": self.listing.event.event_id,
                "splash": self.listing.event.get_cover_picture(),
                "venue": self.showing.venue if self.showing else "Venue TBD"
            },
            "date": {
                "day": self.showing.time.strftime("%a") + ",",
                "day_num": self.showing.time.strftime("%d"),
                "month": self.showing.time.strftime("%b"),
                "year": self.showing.time.strftime("%Y"),
                "time": self.showing.time.strftime("%-I:%M%p")
            } if self.showing else {
                "day": "Date TBD",
                "day_num": "",
                "month": "",
                "year": "",
                "time": "Time TBD"       
            }
        }