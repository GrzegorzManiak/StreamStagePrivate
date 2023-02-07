from django.urls import path
from .views import (
    change_details,
    send_verification
)

urlpatterns = [
    path('change_details/', change_details, name='change_details'),
    path('send_verification/', send_verification, name='send_verification'),
]