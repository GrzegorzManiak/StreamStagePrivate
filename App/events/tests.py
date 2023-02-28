from django.contrib.auth import get_user_model
from django.test import TestCase
from models import Event, EventReview
from views import (
    event_create,
    event_update,
    event_delete,
    event_view,
    get_all_events,
)


# Create your tests here.
# class EventTestCase(TestCase):
#     def setUp(self):
#         self.event_1 = Event.objects.event_create(
#             'title', 
#             'description', 
#             'categories', 
#             'showings', 
#             'media',
#         )


#     def tearDown(self):
