from models import Event, TicketListing, EventShowing
from StreamStage.identifiers import generate_event_id

from .ticketing import add_ticket_listing
from .ticketing import TicketType

def create_event(data):
    event = Event(
        broadcaster = data['broadcaster'],
        title = data['title'],
        description = data['description'],
        over_18s = data['over_18s'],
        event_id = generate_event_id(),
        #live_price = data['live_price']
    )

    add_ticket_listing(event, TicketType.Streaming, data['stream_price'], None)