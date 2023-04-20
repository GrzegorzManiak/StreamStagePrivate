from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Event, EventReview, EventShowing, EventMedia
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

        # Create Test Category
        self.category = Category.objects.create(
            name = 'Test Category',
            description = 'Category Description',
            splash_photo = 'events/Comedy.jfif',
        )
        # Making a variable for calling many-to-many set in later tests
        test_category = Category.objects.all().filter(name='Test Category').first()

        # Create Test Broadcaster
        self.broadcaster = Broadcaster.objects.create(
            handle = 'TestBroadcaster',
            streamer = self.member,
            name = 'Broadcaster',
            biography = 'test biography',
            over_18 = True,
            approved = True
        )

        # Create Test Event
        self.event = Event.objects.create(
            event_id = 'TstEvnt0',
            title = 'Test Event', 
            description = 'description', 
            broadcaster = self.broadcaster, 
            approved = True
        )
        self.event.categories.add(test_category)

        # Create Test Showing 1 - Earlier
        self.showing_next = EventShowing.objects.create(
            event = self.event,
            country = 'AU',
            city = 'Sydney',
            venue = 'Opera House',
            time = '2024-01-28T21:17:06.089Z',
            max_duration = 180
        )

        # Create Test Review 1 - Low Likes, High Rating
        self.review_low = EventReview.objects.create(
            author = self.member,
            event = self.event,
            title = 'Unhappy Review Title', 
            body = 'Review Body',
            rating = 5,
            likes = 2
        )

        # # Create Test Media
        # self.media = EventMedia.objects.create(
        #     event = self.event,
        #     picture = 'events/Comedy.jfif',
        #     description = 'Media Picture Description'
        # )


    # *******************
    # *** Event Tests ***
    # *******************

    # Testing Creation of Event
    def test_event_create(self):
        self.assertEqual(f'{self.event.event_id}', 'TstEvnt0') 
        self.assertEqual(f'{self.event.title}', 'Test Event') 
        self.assertEqual(f'{self.event.description}', 'description') 
        self.assertEqual(f'{self.event.broadcaster}', '@TestBroadcaster') 
        self.assertEqual(f'{self.event.categories.first().name}', 'Test Category') 
        self.assertEqual(f'{self.event.approved}', 'True') 

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html') 

    # Testing Viewing an Event Page
    def test_event_view_page_displays(self):
        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html') 
 

    # Testing Viewing Past Events Page
    def test_get_upcoming_events_page_displays(self):
        # Defining HTTP response & testing if correct
        self.response = self.client.get(reverse('past_events'))
        self.assertEqual(self.response.status_code, 200) 
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event_list_past.html') 

    # Testing Viewing Upcoming Events Page
    def test_get_upcoming_events_page_displays(self):
        # Defining HTTP response & testing if correct
        self.response = self.client.get(reverse('upcoming_events'))
        self.assertEqual(self.response.status_code, 200) 
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event_list_upcoming.html') 

    # Testing Viewing Live Events Page
    def test_get_live_events_page_displays(self):
        # Defining HTTP response & testing if correct
        self.response = self.client.get(reverse('live_events'))
        self.assertEqual(self.response.status_code, 200) 
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event_list_live.html') 

        
    # Testing Updating an Event
    def test_event_update_event_updated(self):
        # Updating Event
        event = Event.objects.get(event_id='TstEvnt0')
        event.title = 'Test Event 2'
        event.description = 'description 2'
        event.save()

        # Testing Updated details of Event
        self.assertEqual(f'{event.event_id}', 'TstEvnt0') 
        self.assertEqual(f'{event.title}', 'Test Event 2') 
        self.assertEqual(f'{event.description}', 'description 2') 

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html') 

    # Testing Deleting an Event
    def test_event_delete_event_deleted(self):
        Event.objects.get(event_id='TstEvnt0').delete()

        # Logging user in as authentication required for deleting event
        self.client.force_login(self.member)

        # Defining HTTP response & testing if correct
        self.response = self.client.get(reverse('member_profile'))

        # self.assertEqual(self.response.status_code, 200)
        # # Testing if correct template used
        self.assertTemplateUsed(self.response, 'profile.html')

    # **************************
    # *** Showing CRUD Tests ***
    # **************************
    
    # Testing Creation of Showing
    def test_showing_create_showing_created(self):
        showing = EventShowing.objects.filter(event='TstEvnt0').first()
        self.assertEqual(f'{showing.country}', 'AU') 
        self.assertEqual(f'{showing.city}', 'Sydney') 
        self.assertEqual(f'{showing.venue}', 'Opera House') 
        self.assertEqual(f'{showing.time}', '2024-01-28 21:17:06.089000+00:00') 
        self.assertEqual(f'{showing.max_duration}', '180') 

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html') 

    # Testing Updating a Showing
    def test_showing_update_showing_updated(self):
        # Updating Showing
        showing = EventShowing.objects.filter(event='TstEvnt0').first()
        showing.country = 'AT'
        showing.city = 'City 2'
        showing.venue = 'Venue 2'
        showing.time = '2024-03-28T22:18:00.089Z'
        showing.max_duration = '200'
        showing.save()

        # Testing Updated details of Showing
        self.assertEqual(f'{showing.country}', 'AT') 
        self.assertEqual(f'{showing.city}', 'City 2') 
        self.assertEqual(f'{showing.venue}', 'Venue 2') 
        self.assertEqual(f'{showing.time}', '2024-03-28T22:18:00.089Z') 
        self.assertEqual(f'{showing.max_duration}', '200') 

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used        
        self.assertTemplateUsed(self.response, 'event.html')

    # Testing Deleting a Showing
    def test_showing_delete_showing_deleted(self):
        EventShowing.objects.get(event='TstEvnt0').delete()

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html')

    # Testing Getting the next Showing
    def test_get_next_showing_next_event_showing_returned(self):
        # Create Test Showing 2 - Later
        self.showing_last = EventShowing.objects.create(
            event = self.event,
            country = 'IE',
            city = 'City',
            venue = 'Venue',
            time = '2024-02-28T21:17:06.089Z',
            max_duration = '300'
        )
        showing = self.event.get_next_showing()

        # Testing if correct next showing is being returned
        self.assertEqual(showing.showing_id, self.showing_next.showing_id)

    # *************************
    # *** Review CRUD Tests ***
    # *************************

    # Testing Creation of Review
    def test_review_create_review_created(self):
        review = EventReview.objects.filter(event='TstEvnt0').first()
        self.assertEqual(f'{review.author}', 'TestMember') 
        self.assertEqual(f'{review.title}', 'Unhappy Review Title') 
        self.assertEqual(f'{review.body}', 'Review Body') 
        self.assertEqual(f'{review.rating}', '5') 
        self.assertEqual(f'{review.likes}', '2') 

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html') 

    # Testing Updating a Review
    def test_review_update_review_updated(self):
        # Updating Review
        review = EventReview.objects.filter(event='TstEvnt0').first()
        review.title = 'Review Title 2'
        review.body = 'Review Body 2'
        review.rating = 3
        review.save()

        # Testing Updated details of Review
        self.assertEqual(f'{review.title}', 'Review Title 2') 
        self.assertEqual(f'{review.body}', 'Review Body 2') 
        self.assertEqual(f'{review.rating}', '3') 

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html')

    # Testing Deleting a Review
    def test_review_delete_review_deleted(self):
        EventReview.objects.filter(event='TstEvnt0').first().delete()

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html')

    # Testing getting highest liked Review
    def test_get_top_review_most_liked_review_returned(self):
        # Create Test Review 2 - High Likes, Low Rating
        self.review_high = EventReview.objects.create(
            author = self.member,
            event = self.event,
            title = 'Review Title', 
            body = 'Review Body',
            rating = 1,
            likes = 10 
        )
        review = self.event.get_top_review()

        # Testing if correct "top" review is being returned
        self.assertEqual(review.review_id, self.review_high.review_id)


    # *******************
    # *** Media Tests ***
    # *******************




