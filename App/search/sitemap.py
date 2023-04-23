# from StreamStage.templatetags import cross_app_reverse
# from events.models import Category
# import datetime

# # -- If no lastmod is specified, the current time is used
# sitemap_entries = [
#     { # -- Home
#         'loc': cross_app_reverse('events', 'searchResult'),
#         'description': 'Search for events, broadcasters, and streamers on StreamStage!',
#         'changefreq': 'daily',
#         'priority': 0.70,
#     },
# ]

# # -- Add all the categories to the sitemap
# for category in Category.objects.all():
#     sitemap_entries.append({
#         'loc': cross_app_reverse('search', 'searchResult') + '?cat=' + category.name,
#         'description': 'Search for events, broadcasters, and streamers in the ' + category.name + ' category on StreamStage!',
#         'changefreq': 'daily',
#         'priority': 0.70,
#         'lastmod': category.updated
#     })
