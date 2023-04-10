from django.urls import path
from .views import SearchResultsListView
from django.conf.urls.static import static
from django.conf import settings

app_name = 'search'

urlpatterns = [
    path('', SearchResultsListView.as_view(), name='searchResult'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)