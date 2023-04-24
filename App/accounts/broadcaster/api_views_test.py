import json
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from StreamStage.templatetags.tags import cross_app_reverse
from accounts.models import Member, Broadcaster
from datetime import datetime, timedelta

from .views import (
    broadcaster_panel,

    update_broadcaster_details,
    get_broadcaster_details,
    fetch_invites,
    send_contribute_invite,
    remove_contributor,
    respond_to_invite
)


class BroadcasterViewsTests(TestCase):
    def setUp(self):
        
        # Create Test Streamer
        self.streamer = Member.objects.create(
            username = 'TestMember1',
            cased_username = "testmember1",
            email = 'test@gmail.com',
            country = 'IE',
            is_streamer = True
        )
        # Create Test Member 2
        self.member2 = Member.objects.create(
            username = 'TestMember2',
            cased_username = "testmember2",
            email = 'test2@gmail.com',
            country = 'IE',
            is_streamer = False
        )

        # Create Test Broadcaster
        self.broadcaster = Broadcaster.objects.create(
            handle = 'TestBroadcaster',
            streamer = self.streamer,
            name = 'Broadcaster',
            biography = 'test biography',
            over_18 = True,
            approved = True
        )

        self.client.force_login(self.streamer)


    # API Tests

    def test_broadcaster_panel(self):
        
        # Querying URL
        self.response = self.client.get(cross_app_reverse('accounts', 'broadcaster_panel'))
        
        # Test that response code is success
        self.assertEqual(self.response.status_code, 200) 

        # Testing if correct template is used
        self.assertTemplateUsed(self.response, 'broadcaster.html') 

    def test_get_broadcaster_details(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'get_broadcaster_details'
        ), {
            'id': self.broadcaster.id
        })

        request.user = self.streamer
        request.csrf_processing_done = True

        # Call view
        response = get_broadcaster_details(request)
        
        # Test if request was successful
        self.assertEqual(response.status_code, 200)

        # Deserialize JSON data
        data = json.loads(response.content)['data']

        details = data['details']
        
        # Test that broadcaster with correct ID was returned
        self.assertEqual(details['id'], str(self.broadcaster.id))
    
    def test_fetch_invites(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'fetch_invites'
        ), {
            'id': self.broadcaster.id
        })

        request.user = self.streamer
        request.csrf_processing_done = True

        # Call view
        response = get_broadcaster_details(request)
        
        # Test if request was successful
        self.assertEqual(response.status_code, 200)

        # Deserialize JSON data
        data = json.loads(response.content)['data']

        details = data['details']
        
        # Test that broadcaster with correct ID was returned
        self.assertEqual(details['id'], str(self.broadcaster.id))
    
    # def test_add_ticket_listing(self):

    #     # Specify data
    #     data = {
    #         'event_id': self.event1.event_id,
    #         'ticket_type': 0,
    #         'stock': 0,
    #         'detail': 'Additional Test Ticket',
    #         'price': 19.99
    #     }

    #     # -- Setup the request
    #     request = RequestFactory()
    #     request = request.post(cross_app_reverse(
    #         'events', 'add_ticket_listing'
    #     ), data)

    #     request.user = self.member
    #     request.csrf_processing_done = True

    #     response = add_ticket_listing(request)

    #     # Test if request was successful
    #     self.assertEqual(response.status_code, 200)

    #     content = json.loads(response.content)

    #     added_id = content['data']['listing']['id']

    #     listing = TicketListing.objects.get(listing_id = added_id)

    #     # Test that listing was added to database
    #     self.assertIsNotNone(listing)

    # def test_del_ticket_listing(self):

    #     listig_id = self.ticket1.listing_id

    #     # Specify data
    #     data = {
    #         'event_id': self.event1.event_id,
    #         'listing_id': listig_id
    #     }

    #     # -- Setup the request
    #     request = RequestFactory()
    #     request = request.post(cross_app_reverse(
    #         'events', 'del_ticket_listing'
    #     ), data)

    #     request.user = self.member
    #     request.csrf_processing_done = True

    #     response = del_ticket_listing(request)

    #     # Test if request was successful
    #     self.assertEqual(response.status_code, 200)

    #     listing = TicketListing.objects.filter(listing_id = listig_id).first()

    #     # Test that listing is no longer present in database
    #     self.assertIsNone(listing)