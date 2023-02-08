from django.urls import path
from .reg_views import (
    recent_view,
    verify_view,
    resend_view,
    verify_view
)

from .ver_views import (
    remove_key_view,
    resend_key_view,
    verify_key_view,
    check_if_verified_recently_view
)

urlpatterns = [
    path('reg/recent/', recent_view, name='reg_recent'),
    path('reg/verify/', verify_view, name='reg_verify'),
    path('reg/resend/', resend_view, name='reg_resend'),
    path('reg/verify/', verify_view, name='reg_verify'),

    path('remove/', remove_key_view, name='remove_key'),
    path('resend/', resend_key_view, name='resend_key'),
    path('verify/', verify_key_view, name='verify_key'),
    path('recent/', check_if_verified_recently_view, name='recent_key'),
]