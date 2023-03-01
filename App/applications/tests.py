from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from applications.models import StreamerApplication, EventApplication, BroadcasterApplication
from accounts.models import Member, Broadcaster
from events.models import Event, Category

from applications.processing import (
    submit_broadcaster_application,
    submit_event_application,
    submit_streamer_application,
    get_broadcaster_application,
    get_streamer_application,
    get_event_applications,

    approve_broadcaster_application,
    reject_broadcaster_application,
    
    approve_event_application,
    reject_event_application,

    approve_streamer_application,
    reject_streamer_application
)


class ApplicationTests(TestCase):
    def setUp(self):
        # Create a test Member that is a streamer
        self.test_streamer = Member(
            username = 'Gediminas_Kreg',
            cased_username = "ged1min4s",
            email = 'gedukas@garblox.com',
            country = 'LT',
            is_streamer = True
        )
        self.test_streamer.save()


        # Create a test Category (for use in the event creation test)
        self.test_category = Category(
            name = "Test Category",
            description = "This is an excellent category",
            splash_photo = 'events/banner.jpg'
        )
        self.test_category.save()


    def test_submit_streamer_application(self):
        test_submission_statement = "I would like to become a streamer!"
        test_applicant = self.test_streamer

        test_data = {
            "submission_statement": test_submission_statement
        }

        submit_streamer_application(test_applicant, test_data)

        application = StreamerApplication.objects.filter(applicant=self.test_streamer).first()

        self.assertTrue(application is not None)
        self.assertEqual(application.submission_statement, test_submission_statement)
    
    def test_submit_broadcaster_application(self):
        test_submission_statement = "I would like to become a broadcaster!"
        test_handle = "TestBroadcaster"
        test_biography = "This is a broadcaster intended to test the system."
        test_name = "Gediminas Kregzde"

        test_applicant = self.test_streamer

        test_data = {
            "submission_statement": test_submission_statement,
            "handle": test_handle,
            "name": test_name,
            "biography": test_biography
        }

        submit_broadcaster_application(test_applicant, test_data)

        application = BroadcasterApplication.objects.filter(applicant=self.test_streamer).first()

        self.assertTrue(application is not None)
        self.assertEqual(application.submission_statement, test_submission_statement)

    def test_submit_event_application(self):
        test_broadcaster = self.broadcaster_or_new()
        test_title = "New Event"
        test_description = "Best event!"
        test_over_18 = False
        test_applicant = self.test_streamer

        test_data = {
            "broadcaster": test_broadcaster,
            "title": test_title,
            "description": test_description,
            "over_18s": test_over_18
        }

        submit_event_application(test_applicant, test_data)

        application = EventApplication.objects.filter(applicant=self.test_streamer).first()

        self.assertTrue(application is not None)
        self.assertEqual(application.event.title, test_title)

    def broadcaster_or_new(self):
        broadcaster = Broadcaster.objects.filter(handle="TestBroadcaster").first()

        if broadcaster is None:
            broadcaster = Broadcaster(
                streamer = self.test_streamer,
                handle = "TestBroadcaster",
                name = "Broady Broad",
                biography = "I'm the coolest!",
                over_18 = False
            )
            broadcaster.save()
    
        return broadcaster



