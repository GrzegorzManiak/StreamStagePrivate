from django.urls import path
from .views import view_event

urlpatterns = [
    path('<slug:event_id>/', view_event, name='view_event'),
]