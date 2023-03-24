from django.urls import path
from .views import index, email

urlpatterns = [
    path('', index, name='homepage_index'),
    path('home/', index, name='homepage_index'),
    path('live/', index, name='homepage_index'),
    path('upcoming', index, name='homepage_index'),
    path('past', index, name='homepage_index'),

    # Temp to view email template
    path('email/', email, name='homepage_email'),
]