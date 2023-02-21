from django.urls import path
from .views import *

urlpatterns = [
    # Events
    path('review/<slug:application_id>/', None, name='new_event'),
    path('apply/', None, name='apply'),
    path('', None, name='landing')
    #Reviews
    # path('<uuid:event_id>/new_review/', ReviewCreateView.as_view(), name='new_review')
]