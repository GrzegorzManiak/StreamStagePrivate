from django.urls import path
from .views import (event_create,
                    event_view,
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
    del_ticket_listing
)

from .ext_api import (
    categorys,
    create_category,
    update_category,
    get_category,
    delete_category, 
    upload_category_image,
    broadcasters,
    get_broadcaster,
    update_broadcaster,
    delete_broadcaster,
    events,
    get_event,
    delete_event,
    update_event
)

urlpatterns = [
    # Events
    path('', get_upcoming_events, name='upcoming_events'),
    path('past/', get_past_events, name='past_events'),
    path('new/', event_create, name='event_new'),
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

    # Admin
    path('api/categorys/', categorys, name='categorys'),
    path('api/categorys/create/', create_category, name='create_category'),
    path('api/categorys/update/', update_category, name='update_category'),
    path('api/categorys/get/', get_category, name='get_category'),
    path('api/categorys/delete/', delete_category, name='delete_category'),
    path('api/categorys/upload_image/', upload_category_image, name='upload_category_image'),

    path('api/broadcasters/', broadcasters, name='broadcasters'),
    path('api/broadcasters/get/', get_broadcaster, name='get_broadcaster'),
    path('api/broadcasters/update/', update_broadcaster, name='update_broadcaster'),
    path('api/broadcasters/delete/', delete_broadcaster, name='delete_broadcaster'),

    path('api/events/', events, name='events'),
    path('api/events/get/', get_event, name='get_event'),
    path('api/events/delete/', delete_event, name='delete_event'),
    path('api/events/update/', update_event, name='update_event'),
]