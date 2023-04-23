# from StreamStage.templatetags import cross_app_reverse
# from accounts.models import Member, Broadcaster
# import datetime

# # -- If no lastmod is specified, the current time is used
# sitemap_entries = [
#     { # -- Home
#         'loc': cross_app_reverse('homepage', 'homepage_index'),
#         'description': 'The homepage of StreamStage!',
#         'changefreq': 'daily',
#         'priority': 0.95,
#     },

#     { # -- Terms of Service
#         'loc': cross_app_reverse('StreamStage', 'render_terms'),
#         'description': 'The terms of service for StreamStage!',
#         'changefreq': 'monthly',
#         'priority': 0.40,
#     },

#     { # -- Privacy Policy
#         'loc': cross_app_reverse('StreamStage', 'render_privacy'),
#         'description': 'The privacy policy for StreamStage!',
#         'changefreq': 'monthly',
#         'priority': 0.40,
#     },

#     { # -- FAQ
#         'loc': cross_app_reverse('StreamStage', 'render_faq'),
#         'description': 'The frequently asked questions for StreamStage!',
#         'changefreq': 'monthly',
#         'priority': 0.50,
#     }
# ]


# # -- Add all user pages to the sitemap
# for user in Member.objects.all():
#     sitemap_entries.append({
#         'loc': cross_app_reverse('homepage', 'user_profile', kwargs={'username': user.cased_username }),
#         'description': user.description,
#         'changefreq': 'daily',
#         'priority': 0.85,
#         'lastmod': user.last_login
#     })

# # -- Add all broadcaster pages to the sitemap
# for broadcaster in Broadcaster.objects.all():
#     sitemap_entries.append({
#         'loc': cross_app_reverse('homepage', 'broadcaster_profile', kwargs={'username': broadcaster.handle }),
#         'description': broadcaster.biography,
#         'changefreq': 'daily',
#         'priority': 0.85,
#         'lastmod': broadcaster.updated
#     })