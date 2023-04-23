from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Event, EventReview, EventShowing, TicketListing, EventMedia, EventTrailer
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
            hex_color = '#FFFFFF',
        )
        # Create Test Category Theatre
        self.category2 = Category.objects.create(
            name = 'Theatre',
            description = 'Category Description',
            splash_photo = 'events/Theatre.jfif',
            hex_color = '#000000',
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

        # Create Test Event 0
        self.event = Event.objects.create(
            event_id = 'TstEvnt0',
            title = 'Test Event', 
            description = 'description', 
            broadcaster = self.broadcaster, 
            approved = True
        )
        self.event.categories.add(self.comedy_category)

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

        # Create Test Showing 1 - Earlier
        self.showing_early = EventShowing.objects.create(
            event = self.event,
            country = 'AU',
            city = 'Sydney',
            venue = 'Opera House',
            time = '2024-01-28T21:17:06.089Z',
            max_duration = 180
        )
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

        # Create Test Review 1 - Low Likes, High Rating
        self.review_low = EventReview.objects.create(
            author = self.member,
            event = self.event,
            title = 'Unhappy Review Title', 
            body = 'Review Body',
            rating = 5,
            likes = 2
        )
        # Create Test Review to test avg rating
        self.review1 = EventReview.objects.create(
            author = self.member,
            event = self.event2,
            title = 'Great', 
            body = 'a',
            rating = 4
        )
        # Create Test Review to test avg rating
        self.review2 = EventReview.objects.create(
            author = self.member,
            event = self.event2,
            title = 'Terrible', 
            body = 'b',
            rating = 2,
            likes = 1,
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
        # Create ticket listing for Test Event 3 (€80, in-person)
        self.ticket3 = TicketListing.objects.create(
            event = self.event3,
            price = 80,
            ticket_type = 1
        )
        # Create ticket listing for Test Event 3 (€100, in-person)
        self.ticket4 = TicketListing.objects.create(
            event = self.event3,
            price = 100,
            ticket_type = 1
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

        # Create Test Trailer
        self.trailer = EventTrailer.objects.create(
            event = self.event3,
            videofile = 'events/Trailer1.mp4',
            description = 'Trailer Description'
        )

        self.client.force_login(self.member)

# *********************
# *** Category Tests ***
# *********************

    # CRUD

    # Testing Creation of Category
    def test_category_create_category_created(self):
        category = Category.objects.first()
        self.assertEqual(f'{category.name}', 'Comedy') 
        self.assertEqual(f'{category.description}', 'Category Description')
        self.assertEqual(f'{category.splash_photo}', 'events/Comedy.jfif')
        self.assertEqual(f'{category.hex_color}', '#FFFFFF') 

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html') 

    # Testing Updating a Category
    def test_category_update_category_updated(self):
        # Updating Category
        category = Category.objects.first()
        category.name = 'Comedy2'
        category.description = 'New Description'
        category.splash_photo = 'events/Music.jpeg'
        category.hex_color = '#EEEEEE'
        category.save()

        # Testing Updated details of Category
        self.assertEqual(f'{category.name}', 'Comedy2') 
        self.assertEqual(f'{category.description}', 'New Description') 
        self.assertEqual(f'{category.splash_photo}', 'events/Music.jpeg')
        self.assertEqual(f'{category.hex_color}', '#EEEEEE') 

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html')

    # Testing Deleting a Category
    def test_category_delete_category_deleted(self):
        Category.objects.first().delete()

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html')



# *******************
# *** Event Tests ***
# *******************

    # CRUD

    # Testing Creation of Event 0
    def test_event_create(self):
        self.assertEqual(f'{self.event.event_id}', 'TstEvnt0') 
        self.assertEqual(f'{self.event.title}', 'Test Event') 
        self.assertEqual(f'{self.event.description}', 'description') 
        self.assertEqual(f'{self.event.broadcaster}', '@TestBroadcaster') 
        self.assertEqual(f'{self.event.categories.first().name}', 'Comedy') 
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

    # Tickets

    # Testing event that has tickets, returns True
    def test_has_ticket_listings_return_true(self):
        self.assertEqual(self.event1.has_ticket_listings(), True)

    # Testing event with no tickets, returns False
    def test_has_ticket_listings_return_false(self):
        self.assertEqual(self.event.has_ticket_listings(), False)

    # Testing min ticket price with no tickets, returns None
    def test_get_min_ticket_price_return_None(self):
        self.assertEqual(self.event.get_min_ticket_price(), None)

    # Testing max ticket price with no tickets, returns None
    def test_get_max_ticket_price_return_None(self):
        self.assertEqual(self.event.get_min_ticket_price(), None)

    # Testing min ticket price, returns ticket with price = 80
    def test_get_min_ticket_price_return_ticket3(self):
        self.assertEqual(self.event3.get_min_ticket_price(), self.ticket3)

    # Testing max ticket price, returns ticket with price = 100
    def test_get_max_ticket_price_return_ticket4(self):
        self.assertEqual(self.event3.get_max_ticket_price(), self.ticket4)


# *********************
# *** Showing Tests ***
# *********************

    # CRUD

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

    # Other

    # Testing if no showings for event, get_showings returns None
    def test_get_showings_no_showing_return_None(self):
        self.assertEqual(self.event3.get_showings().first(), None)

    # Testing if showings for event, returns showings
    def test_get_showings_return_showings(self):
        self.assertEqual(self.event.get_showings().first(), self.showing_late)

    # Testing if no showings for event, get_showings_count returns 0
    def test_get_showings_count_no_showings_return_count(self):
        self.assertEqual(self.event3.get_showings_count(), 0)
        
    # Testing if 2 showing for event, get_showings_count returns 2
    def test_get_showings_count_return_count(self):
        self.assertEqual(self.event2.get_showings_count(), 2)

    # Testing get_upcoming_showings with no showing, returns None
    def test_get_upcoming_showings_return_None(self):
        self.assertEqual(self.event3.get_upcoming_showings().first(), None)

    # Testing get_upcoming_showings with 1 upcoming showing, returns showing
    def test_get_upcoming_showings_return_upcoming_showings(self):
        self.assertEqual(self.event2.get_upcoming_showings().first(), self.showing_upcoming)

    # Testing get_next_showing with no showings, returns None
    def test_get_next_showing_next_event_showing_returned(self):
        self.assertEqual(self.event3.get_next_showing(), None)

    # Testing get_next_showing with 2 showings, returns earlier showing
    def test_get_next_showing_next_event_showing_returned(self):
        # Create Test Showing 2 - Later
        self.showing_late = EventShowing.objects.create(
            event = self.event,
            country = 'IE',
            city = 'City',
            venue = 'Venue',
            time = '2024-02-28T21:17:06.089Z',
            max_duration = 300
        )
        # Testing if correct next showing is being returned
        self.assertEqual(self.event.get_next_showing().showing_id, self.showing_early.showing_id)

    # Testing get_last_showing with no showing, returns None
    def test_get_last_showing_return_None(self):
        self.assertEqual(self.event3.get_last_showing(), None)

    # Testing get_upcoming_showings with showings, returns last
    def test_get_last_showing_return_upcoming_showings(self):
        self.assertEqual(self.event2.get_last_showing(), self.showing_upcoming)

    # Testing is_event_live with event with live showing
    def test_is_event_live_is_live_return_true(self):
        # Create Test Showing - Live
        self.showing_live = EventShowing.objects.create(
            event = self.event2,
            country = 'IE',
            city = 'City',
            venue = 'Venue',
            time = '2023-04-21T20:50:06.089Z',
            max_duration = 300
        )
        self.assertEqual(self.event2.is_event_live(), True)

    # Testing is_event_live with event with live showing
    def test_is_event_live_not_live_return_false(self):
        self.assertEqual(self.event.is_event_live(), False)

# ********************
# *** Review Tests ***
# ********************

    # CRUD

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

    # Other

    # Testing getting reviews

    # Testing if no reviews for event, get_reviews returns None
    def test_get_reviews_no_review_return_None(self):
        self.assertEqual(self.event3.get_reviews().first(), None)

    # Testing if reviews for event, returns reviews
    def test_get_reviews_return_review(self):
        self.assertEqual(self.event.get_reviews().first(), self.review_low)

    # Testing if no reviews for event, get_review_count returns 0
    def test_get_review_count_no_review_return_count(self):
        self.assertEqual(self.event3.get_review_count(), 0)
        
    # Testing if 1 review for event, get_review_count returns 1
    def test_get_review_count_return_count(self):
        self.assertEqual(self.event2.get_review_count(), 2)

    # Testing getting average review of an event based on no review ratings
    def test_get_avg_rating_no_ratings_return_0(self):
        self.assertEqual(self.event3.get_average_rating(), 0)

    # Testing getting average review of an event based on no review ratings
    def test_get_avg_rating_3_rating_return_rating(self):
        self.assertEqual(self.event2.get_average_rating(), 3)


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

    # Testing user_liked with no likers, returns empty list
    def test_user_liked_no_likers_return_false(self):
        self.assertEqual(self.review1.user_liked("John"), False)

    # Testing user_liked with liker in list, returns True
    def test_user_liked_1_liker_return_true(self):
        self.review2.likers.add(self, self.member)
        self.assertEqual(self.review2.user_liked(self.member), True)

    # Testing get_likers_list with no likers, returns empty list
    def test_get_likers_list_no_likers_return_empty(self):
        self.assertEqual(len(self.review1.get_likers_list()), 0)

    # Testing get_likers_list with 1 liker, returns member
    def test_get_likers_list_1_liker_return_liker(self):
        self.review2.likers.add(self.member)
        self.assertEqual(len(self.review2.get_likers_list()), 1)


# *******************
# *** Media Tests ***
# *******************

    # CRUD

    # Testing Creation of Media
    def test_media_create_media_created(self):
        media = EventMedia.objects.filter(event='TstEvnt1').filter()
        self.assertEqual(f'{media.picture}', 'events/Comedy.jfif') 
        self.assertEqual(f'{media.description}', 'Media Picture Description') 

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html') 

    # Testing Updating of Media
    def test_media_update_media_updated(self):
        # Updating Media
        media = EventMedia.objects.filter(event='TstEvnt1').first()
        media.picture = 'events/Theatre.jfif'
        media.description = 'New Description'
        media.save()

        # Testing Updated details of Media
        media = EventMedia.objects.filter(event='TstEvnt1').first()
        self.assertEqual(f'{media.picture}', 'events/Theatre.jfif') 
        self.assertEqual(f'{media.description}', 'New Description') 

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used        
        self.assertTemplateUsed(self.response, 'event.html')

    # Testing Deleting of Media
    def test_media_delete_media_deleted(self):
        EventMedia.objects.get(event='TstEvnt1').delete()

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html')

    # Other

    # Testing if no media for event, default cover_pic returned
    def test_get_cover_picture_no_media_return_default(self):
        self.assertEqual(self.event3.get_cover_picture(), "https://picsum.photos/300/200.jpg")

    # Testing if media for event, cover_pic returned (default 1st pic)
    def test_get_cover_picture_return_cover_pic(self):
        self.assertEqual(self.event1.get_cover_picture(), self.media)

    # Testing if no media for event, get_media returns None
    def test_get_media_no_media_return_None(self):
        self.assertEqual(self.event3.get_media(), None)

    # Testing if media for event, returns media
    def test_get_media_return_media(self):
        media = [self.media2, self.media3]
        self.assertEqual(self.event2.get_media(), media)

    # Testing if no media for event, get_media_count returns 0
    def test_get_media_count_no_media_return_count(self):
        self.assertEqual(self.event3.get_media_count(), 0)
        
    # Testing if 2 media for event, get_media_count returns 2
    def test_get_media_count_return_count(self):
        self.assertEqual(self.event2.get_media_count(), 2)


# *********************
# *** Trailer Tests ***
# *********************

    # CRUD

    # Testing Creation of Trailer
    def test_trailer_create_trailer_created(self):
        trailer = EventTrailer.objects.filter(event='TstEvnt3').first()
        self.assertEqual(f'{trailer.videofile}', 'events/Trailer1.mp4') 
        self.assertEqual(f'{trailer.description}', 'Trailer Description') 

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html') 

    # Testing Updating a Trailer
    def test_trailer_update_trailer_updated(self):
        # Updating Trailer
        trailer = EventTrailer.objects.filter(event='TstEvnt3').first()
        trailer.videofile = 'events/Trailer2.mp4'
        trailer.description = 'New Description'
        trailer.save()

        # Testing Updated details of Trailer
        trailer = EventTrailer.objects.filter(event='TstEvnt3').first()
        self.assertEqual(f'{trailer.videofile}', 'events/Trailer2.mp4') 
        self.assertEqual(f'{trailer.description}', 'New Description') 

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used        
        self.assertTemplateUsed(self.response, 'event.html')

    # Testing Deleting a Trailer
    def test_trailer_delete_trailer_deleted(self):
        EventTrailer.objects.get(event='TstEvnt3').delete()

        # Defining HTTP response & testing if correct
        self.response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        # Testing if correct template used
        self.assertTemplateUsed(self.response, 'event.html')

    # Testing if no trailer for event, get_trailer returns None
    def test_get_trailer_no_trailer_return_emptylist(self):
        self.assertEqual(self.event2.get_trailer().first(), None)

    # Testing if trailer for event, returns trailer
    def test_get_trailer_return_trailer(self):
        self.assertEqual(self.event3.get_trailer().first(), self.trailer)

    # Testing if no trailer for event, get_trailer_count returns 0
    def test_get_trailer_count_no_trailer_return_count(self):
        self.assertEqual(self.event2.get_trailer_count(), 0)
        
    # Testing if 2 trailer for event, get_trailer_count returns 1
    def test_get_trailer_count_return_count(self):
        self.assertEqual(self.event3.get_trailer_count(), 1)
