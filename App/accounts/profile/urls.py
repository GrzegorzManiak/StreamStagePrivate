from django.urls import path
from .views import (
    change_description_view,
    change_username_view,
    send_verification
)

urlpatterns = [
    path('change_username/', change_username_view, name='change_username'),
    path('change_description/', change_description_view, name='change_description'),
    path('send_verification/', send_verification, name='send_verification'),
]