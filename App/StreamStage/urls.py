"""StreamStage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .api.terms import get_latest_terms, create_terms, filter_terms, render_terms, render_terms_specific
from .api.privacy import get_latest_privacy, create_privacy, filter_privacy, render_privacy, render_privacy_specific

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('events/', include('events.urls')),
    path('applications/', include('applications.urls')),
    path('search/', include('search.urls')),
    path('', include('homepage.urls')),
    path('homepage/', include('homepage.urls')),

    # -- API
    path('api/terms/latest', get_latest_terms, name='get_latest_terms'),
    path('api/terms/create', create_terms, name='create_terms'),
    path('api/terms/filter', filter_terms, name='filter_terms'),
    path('terms', render_terms, name='render_terms'),
    path('terms_specific', render_terms_specific, name='render_terms_specific'),

    path('api/privacy/latest', get_latest_privacy, name='get_latest_privacy'),
    path('api/privacy/create', create_privacy, name='create_privacy'),
    path('api/privacy/filter', filter_privacy, name='filter_privacy'),
    path('privacy', render_privacy, name='render_privacy'),
    path('privacy_specific', render_privacy_specific, name='render_privacy_specific'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)