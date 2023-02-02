from django.urls import path
from .oauth import determine_app, OAuthTypes

urlpatterns = [
    path('google/', determine_app(OAuthTypes.GOOGLE), name='google'),
]