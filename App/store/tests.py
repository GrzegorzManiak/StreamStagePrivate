from asyncio import Event
import uuid
from django.test import TestCase

from datetime import datetime
from orders.models import Purchase

from events.models import EventShowing, Event
from accounts.models import Broadcaster, Member
from events.models import Category, TicketListing

from .processing import (
    get_item_price,
    is_in_stock,
    on_intent_success,
    on_subscription_success,
    reverse_items
)

# Create your tests here.

class StoreTests(TestCase):
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

        self.showing = EventShowing.objects.create(
            event = self.event,
            city = "Dublin",
            time = datetime.now(),
            max_duration = 120
        )
        
        # Create ticket listing for Test Event
        self.stream_ticket = TicketListing.objects.create(
            event = self.event,
            price = 1,
        )

        # Create ticket listing for Test Event
        self.live_ticket = TicketListing.objects.create(
            event = self.event,
            showing = self.showing,
            price = 1,
            ticket_type = 1,
            maximum_stock = 100,
            remaining_stock = 100
        )
        # Create ticket listing for Test Event
        self.outofstock_live_ticket = TicketListing.objects.create(
            event = self.event,
            showing = self.showing,
            ticket_type = 1,
            price = 20,
            maximum_stock = 100,
            remaining_stock = 0
        )
    
    def test_get_item_price(self):

        get_price = get_item_price(self.live_ticket.listing_id)

        actual_price = 1

        self.assertEqual(get_price, actual_price)

    def test_is_in_stock(self):

        value = is_in_stock(self.live_ticket.listing_id)

        expected_stock = True

        self.assertEqual(value, expected_stock)

    def test_is_not_in_stock(self):

        value = is_in_stock(self.outofstock_live_ticket.listing_id)

        expected_stock = False

        self.assertEqual(value, expected_stock) 


    def test_reverse_items(self):

        items = [ self.live_ticket, self.stream_ticket ]
        item_ids = [ self.live_ticket.listing_id, self.stream_ticket.listing_id ]

        reversed_items = reverse_items(item_ids)

        for reversed_item in reversed_items:
            self.assertTrue(reversed_item in items)

    def test_intent_success(self):
        
        stock_before = self.live_ticket.remaining_stock

        item = self.live_ticket

        items = [ item.listing_id ]

        stripe_intent = {
            "id": "test-ticket-purchase",
            "payment_method": "test-card"
        }

        cust_intent = {
            "items": items,
            "stripe_intent": stripe_intent,
            "user": self.member
        }

        purchase_id = on_intent_success(cust_intent)

        purchase = Purchase.objects.get(purchase_id = purchase_id)

        # Test if purchase object was created
        self.assertIsNotNone(purchase)

        # Test if stock has gone down
        self.assertLess(TicketListing.objects.get(listing_id=items[0]).remaining_stock, stock_before)

    # def test_on_subscription_success(self):


    #     items = {"data":
    #         {                   
    #             "id": "test-id",

    #             "plan": "ss-monthly",
    #             "amount": 1000,
    #             "interval": "monthly"
    #         }
    #     }
    #     stripe_intent = {
    #         "id": "test-subscription-purchase",
    #         "payment_method": "test-card",
    #         "current_period_start": 100,
    #         "current_period_end": 500,
    #         "items": items
    #     }

    #     cust_intent = {
    #         "items": items,
    #         "stripe_intent": stripe_intent,
    #         "user": self.member,
    #         "payment_method": "card",
    #         "plan": "ss-monthly",
    #     }

    #     on_subscription_success(cust_intent)


