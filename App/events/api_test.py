import json
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from StreamStage.templatetags.tags import cross_app_reverse
from .models import Category, Event, EventReview, EventShowing, TicketListing, EventMedia, EventTrailer
from accounts.models import Member, Broadcaster
from datetime import datetime, timedelta

from .api import (
    del_ticket_listing,
    get_ticket_listings,
    add_ticket_listing,

    get_showings,
    add_showing,
    del_showing,

    get_media,
    add_media,
    del_media,

    get_bc_events
)


class EventAPITests(TestCase):
    def setUp(self):
        # Create Test Member
        self.member = Member.objects.create(
            username = 'TestMember',
            cased_username = "testmember",
            email = 'test@gmail.com',
            country = 'IE',
            is_streamer = True
        )

        # Create Test Category Comedy
        self.category = Category.objects.create(
            name = 'Comedy',
            description = 'Category Description',
            splash_photo = 'events/Comedy.jfif',
            hex_color = '#FFFFFF',
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

        # Create Test Event 1
        self.event1 = Event.objects.create(
            event_id = 'TstEvnt1',
            title = 'Test Event', 
            description = 'Comedy Event', 
            broadcaster = self.broadcaster, 
            approved = True
        )
        self.event1.categories.add(self.category)
                
        # Create Test Event 2
        self.event2 = Event.objects.create(
            event_id = 'TstEvnt2',
            title = 'Test Event 2', 
            description = 'Theatre Event', 
            broadcaster = self.broadcaster, 
            approved = True
        )
        self.event2.categories.add(self.category)

        # Create Test Showing - Past
        self.showing_past = EventShowing.objects.create(
            event = self.event2,
            country = 'AU',
            city = 'Sydney',
            venue = 'Opera House',
            time = '2021-01-28T21:17:06.089Z',
            max_duration = 180
        )
        # Create Test Showing - Upcoming
        self.showing_upcoming = EventShowing.objects.create(
            event = self.event2,
            country = 'AU',
            city = 'Sydney',
            venue = 'Opera House',
            time = '2028-01-28T21:17:06.089Z',
            max_duration = 180
        )

        # Create ticket listing for Test Event 1 (€1)
        self.ticket1 = TicketListing.objects.create(
            event = self.event1,
            price = 1,
        )
        # Create ticket listing for Test Event 2 (€10)
        self.ticket2 = TicketListing.objects.create(
            event = self.event2,
            price = 10,
        )
        
        # Create Test Media (Test Event 1)
        self.media = EventMedia.objects.create(
            event = self.event1,
            picture = 'events/Comedy.jfif',
            description = 'Media Picture Description'
        )        
        # Create Test Media (Test Event 2)
        self.media2 = EventMedia.objects.create(
            event = self.event2,
            picture = 'events/Theatre.jfif',
            description = 'Media 2'
        )
        # Create Test Media (Test Event 2)
        self.media3 = EventMedia.objects.create(
            event = self.event2,
            picture = 'events/Theatre.jfif',
            description = 'Media 2'
        )

        self.client.force_login(self.member)


    # API Tests

    def test_get_ticket_listings(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'events', 'get_ticket_listings'
        ), { 'event_id': self.event1.event_id })

        request.user = self.member
        request.csrf_processing_done = True


        response = get_ticket_listings(request)
        data = json.loads(response.content)['data']

        listings = data['listings']

        # Test - Event 1 should only have one ticket listed.
        self.assertEqual(len(listings), 1)

        # Test - Check if correct ticket details are being returned
        self.assertEqual(listings[0]["id"], str(self.ticket1.listing_id))
    
    def test_add_ticket_listing(self):

        # Specify data
        data = {
            'event_id': self.event1.event_id,
            'ticket_type': 0,
            'stock': 0,
            'detail': 'Additional Test Ticket',
            'price': 19.99
        }

        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'events', 'add_ticket_listing'
        ), data)

        request.user = self.member
        request.csrf_processing_done = True

        response = add_ticket_listing(request)

        # Test if request was successful
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)

        added_id = content['data']['listing']['id']

        listing = TicketListing.objects.get(listing_id = added_id)

        # Test that listing was added to database
        self.assertIsNotNone(listing)

    def test_del_ticket_listing(self):

        listig_id = self.ticket1.listing_id

        # Specify data
        data = {
            'event_id': self.event1.event_id,
            'listing_id': listig_id
        }

        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'events', 'del_ticket_listing'
        ), data)

        request.user = self.member
        request.csrf_processing_done = True

        response = del_ticket_listing(request)

        # Test if request was successful
        self.assertEqual(response.status_code, 200)

        listing = TicketListing.objects.filter(listing_id = listig_id).first()

        # Test that listing is no longer present in database
        self.assertIsNone(listing)

    def test_get_showings(self):

        event_id = self.event2.event_id

        # Specify data
        data = {
            'event_id': event_id
        }

        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'events', 'get_showings'
        ), data)


        request.user = self.member
        request.csrf_processing_done = True

        response = get_showings(request)
        data = json.loads(response.content)['data']

        serialized_showings = data['showings']

        serialized_showing_ids = [ss['showing_id'] for ss in serialized_showings]

        actual_showing_ids = [str(showing.showing_id) for showing in self.event2.get_showings()]

        # Test - Event 2 should have two showings.
        self.assertEqual(len(serialized_showings), 2)

        # Test - Check if correct showings are being returned
        self.assertListEqual(serialized_showing_ids, actual_showing_ids)

    def test_add_showing(self):

        # Specify data
        data = {
            'event_id': self.event1.event_id,
            'time': '2023-03-05T21:23',
            'venue': 'Vicar Street',
            'city': 'Dublin',
            'country': 'Ireland'
        }

        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'events', 'add_showing'
        ), data)

        request.user = self.member
        request.csrf_processing_done = True

        response = add_showing(request)

        # Test if request was successful
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)

        added_id = content['data']['showing']['showing_id']

        # Attempt to retrieve showing from database with returned ID
        showing = EventShowing.objects.get(showing_id = added_id)

        # Test that listing was added to database
        self.assertIsNotNone(showing)

    def test_del_showing(self):

        showing_id = self.event2.get_showings()[0].showing_id

        # Specify data
        data = {
            'event_id': self.event2.event_id,
            'showing_id': showing_id
        }

        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'events', 'del_showing'
        ), data)

        request.user = self.member
        request.csrf_processing_done = True

        response = del_showing(request)

        # Test if request was successful
        self.assertEqual(response.status_code, 200)

        # Attempt to get event showing object with ID we specified
        showing = EventShowing.objects.filter(showing_id = showing_id).first()

        # Test that listing is no longer present in database
        self.assertIsNone(showing)

    
    # Media API tests

    def test_get_media(self):

        event_id = self.event1.event_id

        # Specify data
        data = {
            'event_id': event_id
        }

        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'events', 'get_media'
        ), data)


        request.user = self.member
        request.csrf_processing_done = True

        response = get_media(request)
        data = json.loads(response.content)['data']

        serialized_media = data['media']

        # Test media count
        self.assertEqual(len(serialized_media), self.event1.get_media_count())
        
        # Test equality of media IDs
        self.assertEqual(serialized_media[0]['media_id'], str(self.event1.get_media()[0].media_id))

    def test_add_media(self):

        test_base64_image = ",iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
            
        # Specify data
        data = {
            'event_id': self.event1.event_id,
            'picture': test_base64_image,
            'description': 'Test Picture'
        }

        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'events', 'add_media'
        ), data)

        request.user = self.member
        request.csrf_processing_done = True

        response = add_media(request)

        # Test if request was successful
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)

        added_media = content['data']['media']

        # Attempt to retrieve media object from database with returned ID
        media = EventMedia.objects.get(media_id = added_media['media_id'])

        # Test that media object was created
        self.assertIsNotNone(media)

        # Test that media description is correct
        self.assertEqual(media.description, data['description'])

    def test_del_media(self):

        # Specify event
        event = self.event1

        # select media to delete
        media = self.event1.get_media()[0]
        
        # store media id to test deletion later
        media_id = str(media.media_id)

        # Specify data
        data = {
            'event_id': event.event_id,
            'media_id': media_id
        }

        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'events', 'del_media'
        ), data)

        request.user = self.member
        request.csrf_processing_done = True

        response = del_media(request)

        # Test if request was successful
        self.assertEqual(response.status_code, 200)

        # Attempt to get event showing object with ID we specified
        media = EventMedia.objects.filter(media_id = media_id).first()

        # Test that listing is no longer present in database
        self.assertIsNone(media)

    def test_get_broadcaster_events(self):
        
        broadcaster_id = self.broadcaster.id

        events = [ self.event1.event_id, self.event2.event_id ]

         # Specify data
        data = {
            'broadcaster_id': broadcaster_id,
            'sort': 'rating',
            'order': 'asc',
            'page': '0'
        }

        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'events', 'del_media'
        ), data)

        request.user = self.member
        request.csrf_processing_done = True

        response = get_bc_events(request)
        content = json.loads(response.content)

        serialized_event_ids = [event['event_id'] for event in content['data']['events']]

        # Test if API returned correct event IDs

        self.assertListEqual(serialized_event_ids, events)

