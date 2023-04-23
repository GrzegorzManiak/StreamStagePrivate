from StreamStage.templatetags import cross_app_reverse
import datetime

# -- If no lastmod is specified, the current time is used
sitemap_entries = [
    { # -- Broadcaster Application
        'loc': cross_app_reverse('applications', 'apply_broadcaster'),
        'description': 'Come and join the StreamStage community! Apply to become a Broadcaster!',
        'changefreq': 'monthly',
        'priority': 0.5,
    },

    { # -- Streamer Application
        'loc': cross_app_reverse('applications', 'apply_streamer'),
        'description': 'Come and join the StreamStage community! Apply to become a Streamer!',
        'changefreq': 'monthly',
        'priority': 0.5,
    },

    { # -- Event Application
        'loc': cross_app_reverse('applications', 'apply_event'),
        'description': 'Apply to have your event featured on StreamStage!',
        'changefreq': 'monthly',
        'priority': 0.5,
    },
]