from django.urls import path
from .views import (event_view,
                    get_past_events,
                    get_live_events,
                    get_upcoming_events,
                    event_update,
                    event_delete,
                    review_update,
                    review_delete,
                    review_like,
                    showing_create,
                    showing_update,
                    showing_delete,
)

urlpatterns = [
    # Events
    path('', get_upcoming_events, name='upcoming_events'),
    path('past/', get_past_events, name='past_events'),
    path('live/', get_live_events, name='live_events'),
    path('<slug:event_id>/', event_view, name='event_view'),
    path('<slug:event_id>/update/', event_update, name='event_update'),
    path('<slug:event_id>/delete/', event_delete, name='event_delete'),
    path('<slug:event_id>/showing/new/', showing_create, name='showing_create'),
    path('<slug:event_id>/showing/<slug:showing_id>/update/', showing_update, name='showing_update'),
    path('<slug:event_id>/showing/<slug:showing_id>/delete/', showing_delete, name='showing_delete'),
    path('<slug:event_id>/review/<slug:review_id>/update/', review_update, name='review_update'),
    path('<slug:event_id>/review/<slug:review_id>/delete/', review_delete, name='review_delete'),
    path('review/<slug:review_id>/like', review_like),
]