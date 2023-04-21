from django.test import Client, TestCase
from events.models import Category, Event, TicketListing, EventShowing
from accounts.models import Member, Broadcaster
from datetime import datetime


class EventTests(TestCase):
    def setUp(self):
        # Create Test Member
        self.member = Member.objects.create(
            username = 'TestMember',
            cased_username = "testmember",
            email = 'test@gmail.com',
            country = 'IE',
        )

        # Create Test Category Comedy
        self.category1 = Category.objects.create(
            name = 'Comedy',
            description = 'Category Description',
            splash_photo = 'events/Comedy.jfif',
        )
        # Create Test Category Theatre
        self.category2 = Category.objects.create(
            name = 'Theatre',
            description = 'Category Description',
            splash_photo = 'events/Theatre.jfif',
        )

        # Making a variable for calling many-to-many set in later tests
        self.comedy_category = Category.objects.all().filter(name='Comedy').first()
        self.theatre_category = Category.objects.all().filter(name='Theatre').first()

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
        self.event1.categories.add(self.comedy_category)
                
        # Create Test Event 2
        self.event2 = Event.objects.create(
            event_id = 'TstEvnt2',
            title = 'Test Event 2', 
            description = 'Theatre Event', 
            broadcaster = self.broadcaster, 
            approved = True
        )
        self.event2.categories.add(self.theatre_category)
                
        # Create Test Event 3
        self.event3 = Event.objects.create(
            event_id = 'TstEvnt3',
            title = 'Test Event 3', 
            description = 'Theatre & Comedy Event', 
            broadcaster = self.broadcaster, 
            approved = True
        )
        self.event3.categories.add(self.comedy_category, self.theatre_category)

        # Create Test Event 4 - Today 
        # - Commented out as only used for last test
        # self.event4 = Event.objects.create(
        #     event_id = 'TstEvnt4',
        #     title = 'Test Event 4', 
        #     description = 'Today Event', 
        #     broadcaster = self.broadcaster, 
        #     approved = True
        # )
        # self.event3.categories.add(self.comedy_category)

        # Create showing for Test Event 1 (2022, Ireland)
        self.showing1 = EventShowing.objects.create(
            event = self.event1,
            country = 'IE',
            city = 'Dublin',
            venue = 'The Gate',
            time = '2022-01-01T15:15:03Z',
            max_duration = 120
        )

        # Create showing for Test Event 2 (2024, UK)
        self.showing1 = EventShowing.objects.create(
            event = self.event2,
            country = 'UK',
            city = 'London',
            venue = 'Stratford Hall',
            time = '2024-03-11T15:15:03Z',
            max_duration = 120
        )

        # Create showing for Test Event 3 (2028, Austria)
        self.showing1 = EventShowing.objects.create(
            event = self.event3,
            country = 'AT',
            city = 'Vienna',
            venue = 'The Place',
            time = '2028-12-12T15:15:03Z',
            max_duration = 120
        )
        
        # Create showing for Test Event 4 (Today, Austria)
        #  - Commented out as only used for last test - must change date to today to work
        # self.showing1 = EventShowing.objects.create(
        #     event = self.event4,
        #     country = 'AT',
        #     city = 'Vienna',
        #     venue = 'The Place',
        #     time = '2023-04-21T15:15:03Z',
        #     max_duration = 120
        # )

                # Create ticket listing for Test Event 1 (€1)
        self.ticket1 = TicketListing.objects.create(
            event = self.event1,
            price = 1,
        )

        # Create ticket listing for Test Event 2 (€10)
        self.ticket1 = TicketListing.objects.create(
            event = self.event2,
            price = 10,
        )

        # Create ticket listing for Test Event 3 (€100, in-person)
        self.ticket1 = TicketListing.objects.create(
            event = self.event3,
            price = 100,
            ticket_type = 1
        )

        self.events = [ self.event1, self.event2, self.event3 ]

        self.client = Client()


    # ********************
    # *** Search Tests ***
    # ********************

    # query test category, description, title,
    # query broadcaster handle

    def test_search_query_string_empty(self):
        response = self.client.get('/search/')

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), self.events)

    def test_search_category_comedy(self):
        comedy_category = self.comedy_category

        comedy_events = [
            self.event1,
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('cat=' + comedy_category.name))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), comedy_events)

    def test_search_category_theatre(self):
        theatre_category = self.theatre_category

        theatre_events = [
            self.event2,
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('cat=' + theatre_category.name))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), theatre_events)

    def test_search_query_string_partial_title(self):
        query = "3"

        match_events = [
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('q=' + query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)
    
    def test_search_query_string_partial_category(self):
        query = "com"

        match_events = [
            self.event1,
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('q=' + query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)
    
    def test_search_query_string_partial_description(self):
        query = "comedy event"

        match_events = [
            self.event1,
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('q=' + query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)
    
    def test_search_query_broadcaster_partial_broadcaster_handle(self):
        broadcaster_query = "roadcast"

        match_events = [
            self.event1,
            self.event2,
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('b=' + broadcaster_query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)
    
    def test_search_query_string_partial_broadcaster_name(self):
        broadcaster_query = "roadcast"

        match_events = [
            self.event1,
            self.event2,
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('q=' + broadcaster_query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)    

    def test_search_query_string_no_match(self):
        query = "zombie"

        match_events = [
        ]

        response = self.client.get('/search/', QUERY_STRING = ('q=' + query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)

    def test_search_query_price_between_1_and_100(self):
        query1 = '1'
        query2 = '100'
        match_events = [
            self.event1,
            self.event2,
            self.event3
        ]
        response = self.client.get('/search/', QUERY_STRING = ('mip=' + query1 + '&' + 'map=' + query2))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)

    def test_search_query_price_between_2_and_99(self):
        query1 = '2'
        query2 = '99'
        match_events = [
            self.event2
        ]

        response = self.client.get('/search/', QUERY_STRING = ('mip=' + query1 + '&map=' + query2))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_price_ascending(self):
        query = 'price-asc'
        match_events = [
            self.event1,
            self.event2,
            self.event3
        ]
        response = self.client.get('/search/', QUERY_STRING = ('s=' + query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_price_descending(self):
        query = 'price-desc'
        match_events = [
            self.event3,
            self.event2,
            self.event1
        ]
        response = self.client.get('/search/', QUERY_STRING = ('s=' + query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_date_between_2022_and_2028(self):
        query1 = '01%2F01%2F2022'
        query2 = '01%2F01%2F2029'
        match_events = [
            self.event1,
            self.event2,
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('sd=' + query1 + '&ed=' + query2))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_date_between_2023_and_2027(self):
        query1 = '01%2F01%2F2023'
        query2 = '01%2F01%2F2027'
        match_events = [
            self.event2
        ]

        response = self.client.get('/search/', QUERY_STRING = ('sd=' + query1 + '&ed=' + query2))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_start_date_only_2023(self):
        query = '01%2F01%2F2023'
        match_events = [
            self.event2,
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('sd=' + query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_end_date_only_2023(self):
        query = '01%2F01%2F2023'
        match_events = [
            self.event1
        ]

        response = self.client.get('/search/', QUERY_STRING = ('ed=' + query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_in_person_events_only(self):
        query = 'y'

        match_events = [
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('ip=' + query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_upcoming_events_only(self):
        query = 'y'

        match_events = [
            self.event2
        ]

        response = self.client.get('/search/', QUERY_STRING = ('u=' + query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_country(self):
        query = "Ireland"

        match_events = [
            self.event1
        ]

        response = self.client.get('/search/', QUERY_STRING = ('co=' + query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_city(self):
        query = "London"

        match_events = [
            self.event2
        ]

        response = self.client.get('/search/', QUERY_STRING = ('c=' + query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_venue(self):
        query = "The+Place"

        match_events = [
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('v=' + query))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)

    def test_search_query_venue_city(self):
        query1 = "The+Place"
        query2 = "Vienna"

        match_events = [
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('v=' + query1 + '&c=' + query2))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_venue_city_country(self):
        query1 = "The+Place"
        query2 = "Vienna"
        query3 = "Austria"

        match_events = [
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('v=' + query1 + '&c=' + query2 + '&co=' + query3))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_venue_city_country_in_person(self):
        query1 = "The+Place"
        query2 = "Vienna"
        query3 = "Austria"
        query4 = "y"
        match_events = [
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('ip=' + query4 + '&v=' + query1 + '&c=' + query2 + '&co=' + query3))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_venue_city_country_upcoming_in_person(self):
        query1 = "The+Place"
        query2 = "Vienna"
        query3 = "Austria"
        query4 = "y"

        match_events = [
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('ip=' + query4 + '&v=' + query1 + '&c=' + query2 + '&co=' + query3 + '&ip=' + query4))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    def test_search_query_venue_city_country_upcoming_in_person_category(self):
        query1 = "The+Place"
        query2 = "Vienna"
        query3 = "Austria"
        query4 = "y"
        query5 = self.comedy_category.name

        match_events = [
            self.event3
        ]

        response = self.client.get('/search/', QUERY_STRING = ('ip=' + query4 + '&cat=' + query5 + '&v=' + query1 + '&c=' + query2 + '&co=' + query3 + '&ip=' + query4))

        self.assertEqual(response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(response, 'search.html') 

        # Testing if query set returns all events
        self.assertListEqual(list(response.context['events_list']), match_events)


    # def test_search_query_todays_events_only(self):
    #     query = 'y'

    #     match_events = [
    #         self.event4
    #     ]

    #     response = self.client.get('/search/', QUERY_STRING = ('t=' + query))

    #     self.assertEqual(response.status_code, 200)
    #     # Testing if correct template used
    #     self.assertTemplateUsed(response, 'search.html') 

    #     # Testing if query set returns all events
    #     self.assertListEqual(list(response.context['events_list']), match_events)