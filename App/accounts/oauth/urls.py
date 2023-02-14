from django.urls import path
from .oauth import determine_app, OAuthTypes

urlpatterns = [
    path('google/', determine_app(OAuthTypes.GOOGLE), name='google'),
    path('google/', determine_app(OAuthTypes.GOOGLE), name='discord'),
    path('google/', determine_app(OAuthTypes.GOOGLE), name='github'),
]