from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from applications.models import StreamerApplication, EventApplication, BroadcasterApplication
from accounts.models import Member, Broadcaster
from events.models import Event, Category

from applications.models import STATUS_REJECTED, STATUS_APPROVED, STATUS_WAITING

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
            username = 'ged_kreg',
            email = 'gedukas@garblox.com',
            country = 'LT',
            is_streamer = True
        )
        self.test_streamer.save()

        self.test_admin = Member(
            is_staff = True,
            username = "Admin01",
            email = "admin@streamstage.co",
            country = "IE"
        )
        self.test_admin.save()

        # Create a test Category (for use in the event application creation test)
        self.test_category = Category(
            name = "Test Category",
            description = "This is an excellent category",
            splash_photo = 'events/banner.jpg'
        )
        self.test_category.save()


    def test_submit_streamer_application(self):
        test_submission_statement = "I would like to become a streamer!"
        test_applicant = self.test_streamer

        test_app_data = {
            "submission_statement": test_submission_statement
        }

        submit_streamer_application(test_applicant, test_app_data)

        application = StreamerApplication.objects.filter(applicant=self.test_streamer).first()

        # test that application was created and has correct data
        self.assertTrue(application is not None)
        self.assertEqual(application.submission_statement, test_submission_statement)
        self.assertEqual(application.applicant, test_applicant)
    
    def test_submit_broadcaster_application(self):
        test_submission_statement = "I would like to become a broadcaster!"
        test_handle = "TestBroadcaster"
        test_biography = "This is a broadcaster intended to test the system."
        test_name = "Gediminas Kregzde"

        test_applicant = self.test_streamer

        test_app_data = {
            "submission_statement": test_submission_statement,
            "handle": test_handle,
            "name": test_name,
            "biography": test_biography
        }

        submit_broadcaster_application(test_applicant, test_app_data)

        # query for application
        application = BroadcasterApplication.objects.filter(applicant=self.test_streamer).first()

        self.assertTrue(application is not None)
        self.assertEqual(application.submission_statement, test_submission_statement)
        self.assertEqual(application.broadcaster.handle, test_handle)

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


    def test_approve_streamer_application(self):
        test_streamer_app = self.streamer_app_or_new()

        approve_streamer_application(test_streamer_app, self.test_admin)
        
        self.assertTrue(test_streamer_app.status, STATUS_APPROVED)
        self.assertTrue(test_streamer_app.processed_by, self.test_admin)
    
    def test_reject_streamer_application(self):
        test_streamer_app = self.streamer_app_or_new()

        reject_streamer_application(test_streamer_app, self.test_admin)
        
        self.assertTrue(test_streamer_app.status, STATUS_REJECTED)
        self.assertTrue(test_streamer_app.processed_by, self.test_admin)


    def test_approve_event_application(self):
        test_event_app = self.event_app_or_new()

        approve_event_application(test_event_app, self.test_admin)
        
        self.assertTrue(test_event_app.status, STATUS_APPROVED)
        self.assertTrue(test_event_app.processed_by, self.test_admin)
    
    def test_reject_event_application(self):
        test_event_app = self.event_app_or_new()

        reject_event_application(test_event_app, self.test_admin)
        
        self.assertTrue(test_event_app.status, STATUS_REJECTED)
        self.assertTrue(test_event_app.processed_by, self.test_admin)

    def test_approve_broadcaster_application(self):
        test_broadcaster_app = self.broadcaster_app_or_new()

        approve_broadcaster_application(test_broadcaster_app, self.test_admin)
        
        self.assertTrue(test_broadcaster_app.status, STATUS_APPROVED)
        self.assertTrue(test_broadcaster_app.processed_by, self.test_admin)
    
    def test_reject_broadcaster_application(self):
        test_broadcaster_app = self.broadcaster_app_or_new()

        reject_broadcaster_application(test_broadcaster_app, self.test_admin)
        
        self.assertTrue(test_broadcaster_app.status, STATUS_REJECTED)
        self.assertTrue(test_broadcaster_app.processed_by, self.test_admin)


    def broadcaster_or_new(self):
        broadcaster = Broadcaster.objects.first()

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

    def streamer_app_or_new(self):
        streamer_app = StreamerApplication.objects.first()

        if streamer_app is None:
            streamer_app = StreamerApplication(
                applicant = self.test_streamer,
                submission_statement = "I'd like to become a streamer."
            )

            streamer_app.save()
        
        return streamer_app

    def event_app_or_new(self):
        event_app = EventApplication.objects.first()

        if event_app is None:
            test_broadcaster = self.broadcaster_or_new()

            test_event = Event(
                title = "New Event 02",
                description = "A cool event for tests!",
                broadcaster = test_broadcaster
            )
            test_event.save()

            event_app = EventApplication(
                applicant = self.test_streamer,
                event = test_event
            )
            event_app.save()
        
        return event_app
    
    def broadcaster_app_or_new(self):
        broadcaster_app = BroadcasterApplication.objects.first()

        if broadcaster_app is None:
            test_broadcaster = self.broadcaster_or_new()

            broadcaster_app = BroadcasterApplication(
                applicant = self.test_streamer,
                broadcaster = test_broadcaster
            )
            broadcaster_app.save()
        
        return broadcaster_app