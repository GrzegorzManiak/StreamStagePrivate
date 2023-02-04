from django.urls import path
from .views import view_event, listing

urlpatterns = [
    path('<slug:event_id>/', view_event, name='view_event'),
    path('', listing, name='list_events')
]