"""
    This file will contain all functions to deal with SSO
    and other authentication methods.

    The reason for this is so that we can have a single
    place to look at when we want to change something
    related to authentication, Therefore leaving less
    holes for bugs to sneak in.
"""


# -- Imports
from .oauth.oauth import OAuthTypes, check_oauth_key