"""
    This library contains everything that is needed to handle OAuth
    for StreamStage, this shouldn't really be used by any other
    function outside of the accounts app, so if you're reading this
    and you're not working on the accounts app, you should probably
    not be using this library
"""
from .types import OAuthRespone, OAuthTypes
from .providers import google, github
from .oauth import (
    format_instructions,
    format_providers,
    generate_oauth_key,
    check_oauth_key,
    get_oauth_data,
    get_oauth_user,
    remove_oauth_key,
    clean_key_store,
    determine_app,
    link_oauth_account,
)