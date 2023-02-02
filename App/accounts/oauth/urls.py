from django.urls import path

from . import google_sso

urlpatterns = [
    path('google/', google_sso, name='google'),
]