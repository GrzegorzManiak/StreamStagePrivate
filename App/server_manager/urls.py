from django.urls import path
from .views import (
    announce,
    heartbeat,
    authenticate,
    streams,
)

urlpatterns = [
    path('announce/', announce, name='announce'),
    path('heartbeat/', heartbeat, name='heartbeat'),
    path('authenticate/', authenticate, name='authenticate'),
    path('streams/', streams, name='streams'),
]