from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'me', 'accounts.urls', name='account'),
    host(r'events', 'events.urls', name='events'),
    host(r'master', 'server_manager.urls', name='master'),
    host(r'stream', 'stream.urls', name='stream'),
    host(r'applications', 'applications.urls', name='apps'),
    host(r'(?!www).*', settings.ROOT_URLCONF, name='wildcard'),
)