from django.test import Client, TestCase
from events.models import Category, Event, EventShowing
from accounts.models import Member, Broadcaster


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