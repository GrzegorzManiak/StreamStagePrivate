from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'sso', 'accounts.oauth.urls', name='sso'),
    host(r'(?!www).*', settings.ROOT_URLCONF, name='wildcard'),
)