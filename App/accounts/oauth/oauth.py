from StreamStage import secrets
from django.contrib.auth import get_user_model
from django.apps import apps

import secrets
import datetime

class oAuthRespone():
    SUCCESS = 0
    ERROR = 1
    INVALID = 2
    JSON_ERROR = 3
    REQUEST_ERROR = 4
    EXPIRED = 5
    REDIRECT = 6

    def __str__(self):
        return f"oAuthRespone({str(self.value)})"



"""
    A type for the types of oauth
    that are supported
"""
class OAuthTypes():
    # -- Google, maybe discord and github
    GOOGLE = 0

    # -- Django choices
    choices = (
        (GOOGLE, 'Google'),
    )

    def __str__(self):
        return f"OAuthTypes({str(self.value)})"


    """
        THis function just gets how long the
        token should live for before we 
        call it quits, than the user will have
        to reauthenticate
    """
    def get_ttl(self) -> int:
        match self:
            case OAuthTypes.GOOGLE:
                return secrets.OAUTH_PROVIDERS['google']['ttl']
            
        return 0



"""
    This function returns a formated message instructing the
    Users browser on how to proceed.
"""
def format_instructions(
    email: str,
    email_verified: bool,
    oauth_type: OAuthTypes,
    oauth_id: str
):  
    # -- Lets check if the user has an oauth id 
    # associated with their account
    # NOTE: We cannot directly import the model here
    #       because it will cause a circular import
    oauth_model = apps.get_model('accounts.oAuth2', require_ready=False)

    # -- Check if the user has an oauth id
    exisiting_link = oauth_model.objects.filter(
        id=str(oauth_id),
        oauth_type=oauth_type
    )

    # -- Check if the user has an account
    member = get_user_model().objects.filter(email=email).first()

    has_oauth_id = False
    if exisiting_link.exists() and member is not None:
        # Make sure that the user matches
        if exisiting_link.user == member and exisiting_link.oauth_type == oauth_type:
            has_oauth_id = True


    # -- Return the instructions
    return {
        'has_account': member is not None,
        'email_verified': email_verified,
        'oauth_type': oauth_type,
        'can_authenticate': has_oauth_id,
    }


    
# This is a list of all the oauth requests
# so that once a user has been redirected, they get given
# the same data that they were given from the oauth provider,
# but we also provide a key so that the server can verify
# the validity of the data once they send it back.
authentication_reqests = {}

"""
    Generate a key for a oauth user so the
    server can later on verify the user once
    they have been redirected back to the server

    @param oauth_type: The type of oauth
    @param data: The body of the oauth response
    @return: reference key
"""
def generate_oauth_key(
    oauth_type: OAuthTypes,
    data: dict
) -> str:
    # -- Generate a key
    key = secrets.token_urlsafe(32)

    # -- Add the key to the list
    authentication_reqests[key] = {
        'type': oauth_type,
        'data': data,
        'created': datetime.datetime.now()
    }

    # -- Return the key
    return key



"""
    Check if the key expired 
    and remove it from the list

    @param key: The key to check
    @return: True if the key is valid, False if not
"""
def check_oauth_key(key: str) -> bool:
    # -- Check if the key exists
    if key not in authentication_reqests:
        return False

    # -- Check if the key is expired
    created = authentication_reqests[key]['created']
    ttl = OAuthTypes.get_ttl(authentication_reqests[key]['type'])

    if (created + ttl) < datetime.datetime.now():
        del authentication_reqests[key]
        return False

    # -- Key is valid
    return True



"""
    Loop trough all the keys to check if 
    any of them became expired
"""
def clean_key_store():
    for key in authentication_reqests:
        check_oauth_key(key)
