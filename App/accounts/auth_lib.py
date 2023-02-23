"""
    This file will contain all functions to deal with SSO
    and other authentication methods.

    The reason for this is so that we can have a single
    place to look at when we want to change something
    related to authentication, Therefore leaving less
    holes for bugs to sneak in.
"""


# -- Imports
import secrets
import time

from .models import Member
from .oauth import (
    check_oauth_key,
    get_oauth_data,
    get_oauth_user,
    remove_oauth_key,
)


# 15 minutes
TTL = 60 * 15

"""
    Just a simple class to hold the key types
    aka, email and oauth
"""
class KeyType():
    OAUTH = 'oauth'
    EMAIL = 'email'

    def new(self):
        return self.__class__()

    def __str__(self):
        return self.__class__.__name__

    def assign_key(self, key: str):
        self.key = key

    def get_key(self):
        return self.key



authentication_keys = {}

"""
    Generate a key for the user to use to
    authenticate with
"""
def generate_key(member: Member) -> str:
    # -- Generate a key
    key = f'EMAIL:{secrets.token_urlsafe(32)}'

    # -- Add the key to the dictionary
    authentication_keys[key] = {
        'member': member,
        'created': time.time()
    }

    return key
    

"""
    Check if the key is valid
"""
def check_key(key: str) -> bool:
    # -- Check if the key exists
    if key not in authentication_keys:
        return False

    # -- Check if the key has expired
    if time.time() - authentication_keys[key]['created'] > TTL:
        del authentication_keys[key]
        return False

    # -- The key is valid
    return True



"""
    Consumes the key and returns the member
    if the key is valid
"""
def consume_key(key: str) -> Member or None:
    # -- Check if the key is valid
    if not check_key(key):
        return None

    # -- Get the member
    member = authentication_keys[key]['member']

    # -- Remove the key from the dictionary
    del authentication_keys[key]

    # -- Return the member
    return member



"""
    This function will be used to determine what
    key the user is trying to use to authenticate
    with.
"""
def determine_key(key: str) -> KeyType or None:
    # -- Make sure the key is not empty
    if not key: return None

    # -- Split the key by the first ':'
    identifier = key.split(':', 1)
    if len(identifier) != 2: return None
    identifier = identifier[0].lower()

    match identifier:
        case 'oauth': 
            # -- Check if the key is valid
            if not check_oauth_key(key): return None
            return KeyType.OAUTH

        case 'email': 
            # -- Check if the key is valid
            if not check_key(key): return None
            return KeyType.EMAIL

        case _: return None



"""
    This function will be used to authenticate
    the user with the key that they have provided
"""
def authenticate_key(key: str) -> Member or None:
    # -- Determine the key type
    keytype = determine_key(key)
    if keytype is None: return None


    # -- Authenticate the user
    match keytype:
        case KeyType.OAUTH:
            # -- Get the oauth data
            data = check_oauth_key(key)

            # -- Check if the user is valid
            if data == False: return None

            # -- Get the user
            oauth_data = get_oauth_data(key)

            # -- Get the user
            user = get_oauth_user(
                oauth_data['oauth_id'],
                oauth_data['type']
            )

            # -- Remove the key
            remove_oauth_key(key)

            # -- Check if the user is valid
            if not user: return None

        case KeyType.EMAIL:
            # -- Get the user
            user = consume_key(key)

            # -- Check if the user is valid
            if not user: return None 


    return user


