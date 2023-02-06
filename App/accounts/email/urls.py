from django.urls import path
from .reg_views import (
    recent_view,
    verify_view,
    resend_view,
    verify_view
)

urlpatterns = [
    path('reg/recent/', recent_view, name='reg_recent'),
    path('reg/verify/', verify_view, name='reg_verify'),
    path('reg/resend/', resend_view, name='reg_resend'),
    path('reg/verify/', verify_view, name='reg_verify'),
]