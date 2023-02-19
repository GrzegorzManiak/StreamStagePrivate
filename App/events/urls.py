from django.urls import path
from .views import (event_create,
                    event_view,
                    get_all_events,
                    event_update,
                    event_delete,
                    review_create,
                    review_update,
                    review_delete,
                    # get_all_reviews,
)

urlpatterns = [
    # Events
    path('', get_all_events, name='all_events'),
    path('new/', event_create, name='event_new'),
    path('<slug:event_id>/', event_view, name='event_view'),
    path('<slug:event_id>/update/', event_update, name='event_update'),
    path('<slug:event_id>/delete/', event_delete, name='event_delete'),
    path('<slug:event_id>/delete_review/', review_delete, name='review_delete'),
]