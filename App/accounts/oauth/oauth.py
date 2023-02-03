from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework import status
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model
from django.apps import apps

from .google import Google
from .types import OAuthTypes, OAuthRespone

import secrets
import time


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
    ).first()

    # -- Check if the user has an account
    member = get_user_model().objects.filter(email=email).first()

    has_oauth_id = False
    if exisiting_link is not None and member is not None:
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
    data: dict,
    created: float = time.time()
) -> str:
    # -- Generate a key
    key = f'OAUTH_{oauth_type}_{secrets.token_urlsafe(32)}'

    # -- Add the key to the list
    authentication_reqests[key] = {
        'type': oauth_type,
        'data': data,
        'created': created
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

    if (created + ttl) < time.time():
        del authentication_reqests[key]
        return False

    # -- Key is valid
    return True



"""
    Get the oauth data from the key
"""
def get_oauth_data(key: str) -> dict or None:
    # -- Check if the key is valid
    if not check_oauth_key(key):
        return None

    # -- Get the data
    data = authentication_reqests[key]['data']

    # -- Return the data
    return data



"""
    Remove the key from the list
"""
def remove_oauth_key(key: str) -> bool:
    # -- Check if the key is valid
    if not check_oauth_key(key):
        return False

    # -- Remove the key
    del authentication_reqests[key]

    # -- Return true since the key was removed
    return True



"""
    Loop trough all the keys to check if 
    any of them became expired
"""
def clean_key_store():
    # -- Loop trough all the keys
    #    But we have to be careful because
    #    we are modifying the list while
    #    looping trough it
    keys = list(authentication_reqests.keys())
    for key in keys:
        check_oauth_key(key)

    


"""
    This is the OAuth view that is used to
    determine what service the user is trying
    to authenticate with
"""
def determine_app(oauth_service: OAuthTypes):
    app = None

    # -- Determine the app
    match oauth_service:
        case OAuthTypes.GOOGLE: app = Google


    @api_view(['GET'])
    def sso(request):
        # -- Check if the user is already authenticated
        if request.user.is_authenticated:
            return reverse_lazy('login')
        

        # -- Get the code from the request
        #    And if its none, just redirect
        #    The user to the oauth url
        code = request.GET.get('code')
        if code == None:
            return HttpResponseRedirect(app().url)


        # -- Create a new Google object
        choosen_app = app(code)

        # -- Get the access token
        res = choosen_app.get_access_token()
        if res != OAuthRespone.SUCCESS:
            return JsonResponse({'message': str(res)}, 
            status=status.HTTP_400_BAD_REQUEST)

        # -- Get the user info
        res = choosen_app.get_userinfo()
        if res != OAuthRespone.SUCCESS:
            return JsonResponse({'message': str(res)}, 
            status=status.HTTP_400_BAD_REQUEST)


        # -- Generate a reference key
        #    So that we can fetch this
        #    User later on
        key = generate_oauth_key(
            oauth_service,
            choosen_app.user.serialize()
        )


        # -- Return success
        return JsonResponse({
            'message': 'Success',
            'user': choosen_app.user.serialize(),
            'token': key,
            'instructions': format_instructions(
                choosen_app.user.get_email(),
                choosen_app.user.get_is_verified(),
                oauth_service,
                choosen_app.user.get_id()
            )
        }, status=status.HTTP_200_OK)

    return sso