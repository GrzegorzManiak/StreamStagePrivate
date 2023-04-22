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
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from .api.terms import get_latest_terms, create_terms, filter_terms, render_terms, render_terms_specific
from .api.privacy import get_latest_privacy, create_privacy, filter_privacy, render_privacy, render_privacy_specific
from .api.faq import create_faq, filter_faq, render_faq, delete_faq, update_faq
from .views import about_us_view

from accounts.sitemap import sitemap_entries as acc_se
from applications.sitemap import sitemap_entries as app_se
from events.sitemap import sitemap_entries as ev_se
from homepage.sitemap import sitemap_entries as hp_se
from search.sitemap import sitemap_entries as sr_se

# -- Combine all the sitemaps
sitemap_entries = [
    *acc_se,
    *app_se,
    *ev_se,
    *hp_se,
    *sr_se
]

formated_sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

# -- Process the sitemaps
for sitemap_entry in sitemap_entries:
    lastmod = None
    if 'lastmod' in sitemap_entry:
        lastmod = sitemap_entry['lastmod']
        lastmod = lastmod.strftime('%Y-%m-%d')

    else: lastmod = datetime.datetime.now().strftime('%Y-%m-%d')
        
    entry = f"""    <url>
        <loc>{sitemap_entry['loc']}</loc>
        <lastmod>{lastmod}</lastmod>
        { f"<changefreq>{sitemap_entry['changefreq']}</changefreq>" if 'changefreq' in sitemap_entry else '' }
        { f"<priority>{sitemap_entry['priority']}</priority>" if 'priority' in sitemap_entry else '' }
    </url>\n"""

    formated_sitemap += entry

formated_sitemap += f"""</urlset>"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('events/', include('events.urls')),
    path('applications/', include('applications.urls')),
    path('search/', include('search.urls')),
    path('', include('homepage.urls')),
    path('homepage/', include('homepage.urls')),
    path('about_us', about_us_view, name='about_us'),

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

    path('api/faq/create', create_faq, name='create_faq'),
    path('api/faq/filter', filter_faq, name='filter_faq'),
    path('api/faq/delete', delete_faq, name='delete_faq'),
    path('api/faq/update', update_faq, name='update_faq'),
    path('faq', render_faq, name='render_faq'),

    path("sitemap.xml", 
        (lambda r: HttpResponse(formated_sitemap, content_type="application/xml")), 
        name="sitemap"
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)