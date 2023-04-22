from StreamStage.templatetags import cross_app_reverse
from .models import Event
import datetime

# -- If no lastmod is specified, the current time is used
sitemap_entries = [
    { # -- Upcoming Events
        'loc': cross_app_reverse('events', 'upcoming_events'),
        'description': 'View all the super cool upcoming events on StreamStage!',
        'changefreq': 'daily',
        'priority': 0.8,
    },

    { # -- Past Events
        'loc': cross_app_reverse('events', 'past_events'),
        'description': 'View all the super cool past events on StreamStage!',
        'changefreq': 'daily',
        'priority': 0.75,
    },

    { # -- Live Events
        'loc': cross_app_reverse('events', 'live_events'),
        'description': 'View all the super cool currently live events on StreamStage!',
        'changefreq': 'daily',
        'priority': 0.90,
    }
]

# -- Add all events to the sitemap
for event in Event.objects.all():
    sitemap_entries.append({
        'loc': event.get_absolute_url(),
        'description': event.description,
        'changefreq': 'daily',
        'priority': 0.85,
        'lastmod': event.updated,
    })