from django.urls import path
from .views import (
    index,
    ingests
)

urlpatterns = [
    path('', index, name='index'),
    path('ingests', ingests, name='ingests'),
]