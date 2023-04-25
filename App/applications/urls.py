from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

from .api import (
    get_user_applications,
    update_application_status,
    fetch_pending_applications
)

urlpatterns = [
    # Events
    #path('review/<slug:application_id>/', None, name='review_application'),
    path('broadcaster', apply_broadcaster, name="apply_broadcaster"),
    path('streamer', apply_streamer, name="apply_streamer"),
    path('event', apply_event, name="apply_event"),
    path('admin/', list_applications, name="review_applications"),
    path('streamer/<slug:id>/', review_streamer_application, name="review_streamer_application"),
    path('broadcaster/<slug:id>/', review_broadcaster_application, name="review_broadcaster_application"),
    path('events/<slug:id>/', review_event_application, name="review_event_application"),
    path('', landing_url, name='landing'),
    #Reviews
    # path('<uuid:event_id>/new_review/', ReviewCreateView.as_view(), name='new_review')


    # API

    path('admin/api/get_applications', get_user_applications, name='get_user_applications'),
    path('admin/api/update_status', update_application_status, name='update_application_status'),
    path('admin/api/fetch_applications', fetch_pending_applications, name='fetch_applications')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)