from django.urls import path
from .views import (
    index, 
    email, 
    broadcaster_profile, 
    user_profile
)

from django.conf import settings
from django.conf.urls.static import static
from accounts.other import submit_report

urlpatterns = [
    path('', index, name='homepage_index'),
    path('home/', index, name='homepage_index'),
    path('live/', index, name='homepage_index'),
    path('upcoming', index, name='homepage_index'),
    path('past', index, name='homepage_index'),

    path('api/submit_report/', submit_report, name='submit_report'),

    # -- Profiles
    path('u/@<str:username>', user_profile, name='user_profile'),
    path('b/@<str:username>', broadcaster_profile, name='broadcaster_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)