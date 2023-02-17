from django.urls import path
from .views import (event_create,
                    event_view,
                    get_all_events,
                    event_update,
                    event_delete,
                    ReviewCreateView,
                    ReviewDetailView,
                    # get_all_reviews,
                    ReviewUpdateView,
                    ReviewDeleteView
)

urlpatterns = [
    # Events
    path('new/', event_create, name='event_new'),
    path('<slug:event_id>/', event_view, name='event_view'),
    path('', get_all_events, name='all_events'),
    path('<slug:event_id>/edit/', event_update, name='event_update'),
    path('<slug:event_id>/delete/', event_delete, name='event_delete'),
    path('<slug:event_id>/new_review/', ReviewCreateView.as_view(), name='new_review')
]