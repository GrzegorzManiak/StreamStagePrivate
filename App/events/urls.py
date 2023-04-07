from django.urls import path
from .views import (event_view,
                    get_past_events,
                    get_upcoming_events,
                    event_update,
                    event_delete,
                    review_create,
                    review_update,
                    review_delete,
                    review_like,
                    showing_create,
                    showing_update,
                    showing_delete
)

from .api import (
    get_ticket_listings,
    add_ticket_listing,
    del_ticket_listing,

    get_showings,
    add_showing,
    del_showing,

    get_media,
    add_media,
    del_media
)

urlpatterns = [
    # Events
    path('', get_upcoming_events, name='upcoming_events'),
    path('past/', get_past_events, name='past_events'),
    path('<slug:event_id>/', event_view, name='event_view'),
    path('<slug:event_id>/update/', event_update, name='event_update'),
    path('<slug:event_id>/delete/', event_delete, name='event_delete'),
    path('<slug:event_id>/showing/new/', showing_create, name='showing_create'),
    path('<slug:event_id>/showing/<slug:showing_id>/update/', showing_update, name='showing_update'),
    path('<slug:event_id>/showing/<slug:showing_id>/delete/', showing_delete, name='showing_delete'),
    path('<slug:event_id>/review/<slug:review_id>/update/', review_update, name='review_update'),
    path('<slug:event_id>/review/<slug:review_id>/delete/', review_delete, name='review_delete'),
    path('review/<slug:review_id>/like', review_like),

    # API
    path('api/get_ticket_listings', get_ticket_listings, name='get_ticket_listings'),
    path('api/add_ticket_listings', add_ticket_listing, name='add_ticket_listing'),
    path('api/del_ticket_listings', del_ticket_listing, name='del_ticket_listing'),

    path('api/get_showings', get_showings, name='get_showings'),
    path('api/add_showings', add_showing, name='add_showing'),
    path('api/del_showings', del_showing, name='del_showing'),

    path('api/get_media', get_media, name='get_media'),
    path('api/add_media', add_media, name='add_media'),
    path('api/del_media', del_media, name='del_media'),
]