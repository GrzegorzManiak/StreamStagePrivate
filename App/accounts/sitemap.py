from StreamStage.templatetags import cross_app_reverse
import datetime

# -- If no lastmod is specified, the current time is used
sitemap_entries = [
    { # -- Login
        'loc': cross_app_reverse('accounts', 'login'),
        'changefreq': 'monthly',
        'priority': 0.65,
    },

    { # -- Register
        'loc': cross_app_reverse('accounts', 'register'),
        'changefreq': 'monthly',
        'priority': 0.65,
    },

    { # -- Forgot Details
        'loc': cross_app_reverse('accounts', 'forgot'),
        'changefreq': 'monthly',
        'priority': 0.65,
    },

    { # -- Profile
        'loc': cross_app_reverse('accounts', 'member_profile'),
        'changefreq': 'monthly',
        'priority': 0.70,
    },

    { # -- Google OAuth
        'loc': cross_app_reverse('accounts', 'google'),
        'changefreq': 'yearly',
        'priority': 0.65,
    },

    { # -- Discord OAuth
        'loc': cross_app_reverse('accounts', 'discord'),
        'changefreq': 'yearly',
        'priority': 0.65,
    },

    { # -- Github OAuth
        'loc': cross_app_reverse('accounts', 'github'),
        'changefreq': 'yearly',
        'priority': 0.65,
    },

    { # -- Broadcaster Panel
        'loc': cross_app_reverse('accounts', 'broadcaster_panel'),
        'changefreq': 'monthly',
        'priority': 0.70,
    },
]