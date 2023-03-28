from django.test import TestCase, RequestFactory
from .views import SearchResultsListView
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
        comedy_category = Category.objects.all().filter(name='Comedy').first()
        theatre_category = Category.objects.all().filter(name='Theatre').first()

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
        self.event1.categories.add(comedy_category)
                
        # Create Test Event 2
        self.event2 = Event.objects.create(
            event_id = 'TstEvnt2',
            title = 'Test Event 2', 
            description = 'Theatre Event', 
            broadcaster = self.broadcaster, 
            approved = True
        )
        self.event2.categories.add(theatre_category)
                
        # Create Test Event 3
        self.event3 = Event.objects.create(
            event_id = 'TstEvnt3',
            title = 'Test Event 3', 
            description = 'Theatre & Comedy Event', 
            broadcaster = self.broadcaster, 
            approved = True
        )
        self.event3.categories.add(comedy_category, theatre_category)


    # ********************
    # *** Search Tests ***
    # ********************

    def test_get_queryset_displays_search_results(self):
        request = RequestFactory().get('/search')
        view = SearchResultsListView()
        qs = view.get_queryset
        self.assertQuerysetEqual(qs, results())

        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'search.html') 