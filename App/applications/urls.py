from django.urls import path
from .views import *

urlpatterns = [
    # Events
    #path('review/<slug:application_id>/', None, name='review_application'),
    path('apply/', apply_for_event, name='apply'),
    path('broadcaster', apply_broadcaster, name="apply_broadcaster"),
    path('streamer', apply_streamer, name="apply_streamer"),
    path('event', apply_event, name="apply_event"),
    path('', landing_url, name='landing')
    #Reviews
    # path('<uuid:event_id>/new_review/', ReviewCreateView.as_view(), name='new_review')
]