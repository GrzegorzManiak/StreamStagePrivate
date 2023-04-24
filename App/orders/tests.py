import uuid
from django.test import TestCase

from .models import Purchase
from accounts.models import Broadcaster, Member
from events.models import TicketListing, Event

from .processing import create_purchase

# Create your tests here.
class TestOrders(TestCase):
    def setUp(self):
        # Create Test Member
        self.member = Member.objects.create(
            username = 'TestMember',
            cased_username = "testmember",
            email = 'test@gmail.com',
            country = 'IE',
        )
        
        # Create Test Broadcaster
        self.broadcaster = Broadcaster.objects.create(
            handle = 'TestBroadcaster',
            streamer = self.member,
            name = 'Broadcaster',
            biography = 'test biography',
            over_18 = True,
            approved = True
        )

        # Create Test Event 0
        self.event = Event.objects.create(
            event_id = 'TstEvnt0',
            title = 'Test Event', 
            description = 'description', 
            broadcaster = self.broadcaster, 
            approved = True
        )
        
        # Create ticket listing for Test Event
        self.stream_ticket = TicketListing.objects.create(
            event = self.event,
            price = 1,
        )

    def test_create_purchase(self):
        purchase_id = uuid.uuid4()

        stripe_intent = {
            "id": "test-id",
            "payment_method": "test-card"
        }

        purchaser = self.member

        billing_data = {
            "billingName": "Joe Mulvaney",
            "billingAddress1": "40 Mulvay",
            "billingCity": "City",
            "billingPostcode": "3024",
            "billingCountry": "Venezuela",
        }

        ticket_listing = self.stream_ticket

        total_mult = 1

        create_purchase(purchase_id, stripe_intent, purchaser, billing_data, ticket_listing, total_mult)

        purchase = Purchase.objects.get(purchase_id = purchase_id)

        # test if purchase object was created
        self.assertIsNotNone(purchase)

        # test if there are items in this purchase
        self.assertTrue(purchase.get_items().count() > 0)
