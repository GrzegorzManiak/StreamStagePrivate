from django.urls import path
from .views import (EventCreateView,
                    view_event,
                    get_all_events,
                    EventUpdateView,
                    EventDeleteView,
                    ReviewCreateView,
                    ReviewDetailView,
                    # get_all_reviews,
                    ReviewUpdateView,
                    ReviewDeleteView
)

urlpatterns = [
    # Events
    path('new/', EventCreateView.as_view(), name='new_event'),
    path('<slug:event_id>/', view_event, name='view_event'),
    path('', get_all_events, name='all_events')
    #Reviews
    # path('<uuid:event_id>/new_review/', ReviewCreateView.as_view(), name='new_review')
]