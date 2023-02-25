import base64
import json
import secrets
import time

from django.apps import apps
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from rest_framework import status

from django.urls import reverse, reverse_lazy
from rest_framework.decorators import api_view

from .providers import google, github, discord
from .types import OAuthRespone, OAuthTypes


"""
    This function returns a formated message instructing the
    Users browser on how to proceed.
"""
def format_instructions(
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
        oauth_id=str(oauth_id),
        oauth_type=oauth_type
    ).first()

    has_oauth_id = False
    if exisiting_link is not None:
            has_oauth_id = True


    # -- Return the instructions
    return {
        'has_account': exisiting_link is not None,
        'email_verified': email_verified,
        'oauth_type': oauth_type,
        'can_authenticate': has_oauth_id,
        'needs_username': has_oauth_id is False,
        'needs_password': has_oauth_id is False,
        'needs_email': email_verified is False,
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
    oauth_id: str,
    created: float = time.time()
) -> str:
    # -- Generate a key
    key = f'OAUTH:{oauth_type}:{secrets.token_urlsafe(32)}'

    # -- Add the key to the list
    authentication_reqests[key] = {
        'type': oauth_type,
        'data': data,
        'created': created,
        'oauth_id': oauth_id
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

    
    # -- Now make sure that the key exists in
    #    the oauth model
    oauth_model = apps.get_model('accounts.oAuth2')
    entry = oauth_model.objects.filter(
        oauth_id=authentication_reqests[key]['oauth_id'],
        oauth_type=authentication_reqests[key]['type']
    ).first()

    # -- Check if the key exists
    if entry is None:
        return False
    
    entry.last_used = time.time()
    entry.save()

    # -- Key is valid
    return True



"""
    Get the user from the ID not the KEY
    very important distinction.
"""
def get_oauth_user(oauth_id: str, oauth_type: OAuthTypes):
    # -- Get the oauth model
    oauth_model = apps.get_model('accounts.oAuth2')

    # -- Get the user
    user = oauth_model.objects.filter(
        oauth_id=oauth_id,
        oauth_type=oauth_type
    ).first()

    # -- Return the user
    return user.user



"""
    Get the oauth data from the key
"""
def get_oauth_data(key: str) -> dict or None:
    # -- Check if the key is valid
    if key not in authentication_reqests:
        return None

    # -- Get the data
    data = authentication_reqests[key]

    # -- Return the data
    return data



"""
    Remove the key from the list
"""
def remove_oauth_key(key: str) -> bool:
    # -- Check if the key is valid
    if key not in authentication_reqests:
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
        case OAuthTypes.GOOGLE: app = google
        case OAuthTypes.GITHUB: app = github
        case OAuthTypes.DISCORD: app = discord


    @api_view(['GET'])
    def sso(request):
        # -- Check if the user is already authenticated
        if request.user.is_authenticated:
            return reverse('login')

        # -- Get the code from the request
        #    And if its none, just redirect
        #    The user to the oauth url
        code = request.GET.get('code')
        if code == None:
            return HttpResponseRedirect(app.Oauth().url)


        # -- Create a new Google object
        choosen_app = app.Oauth(code)

        # -- Get the access token
        res = choosen_app.get_access_token()
        if res != OAuthRespone.SUCCESS:
            response = HttpResponseRedirect(reverse('login'))
            response.set_cookie('oauth_error', str(res))

            return response

        # -- Get the user info
        res = choosen_app.get_userinfo()
        if res != OAuthRespone.SUCCESS:
            response = HttpResponseRedirect(reverse('login'))
            response.set_cookie('oauth_error', str(res))

            return response

        # -- Generate a reference key
        #    So that we can fetch this
        #    User later on
        key = generate_oauth_key(
            oauth_service,
            choosen_app.user.serialize(),
            str(choosen_app.user.get_id())
        )

        # -- Format the instructions
        instructions = {
            'message': 'Success',
            'user': choosen_app.user.serialize(),
            'token': key,
            'instructions': format_instructions(
                choosen_app.user.get_is_verified(),
                oauth_service,
                choosen_app.user.get_id()
            )
        }

        # -- Convert the instructions to json
        instructions = json.dumps(instructions)
        enocded_instructions = base64.b64encode(instructions.encode('utf-8')).decode('utf-8')

        # -- Return the instructions
        return HttpResponseRedirect(
            reverse_lazy('login') + f'?instructions={enocded_instructions}'
        )

    return sso



"""
    This function formats all available
    oauth options for django templates to use
"""
def format_providers():

    # -- Format the providers
    providers = []
    for provider in OAuthTypes.choices:
        providers.append({
            'name': provider[1],
            'id': provider[1].lower(),
            'url': reverse(provider[1].lower())
        })

    return providers



"""
    This function links the user to the oauth
    account
"""
def link_oauth_account(user, oauth_key: str):
    # -- Get the oauth data
    oauth_data = get_oauth_data(oauth_key)

    # -- Check if the key is valid
    if oauth_data == None:
        return False

    # -- Make sure the user is valid
    if user == None:
        return False

    # -- Remove the key
    remove_oauth_key(oauth_key)

    # -- Get the oauth model
    oauth_model = apps.get_model('accounts.oAuth2')

    try:
        # -- Create the oauth model
        oauth_model.objects.create(
            user=user,
            oauth_id=oauth_data['oauth_id'],
            oauth_type=oauth_data['type']
        )

    except:
        return False



"""
    :name: get_all_oauth_for_member
    :description: This function gets all the oauth
        linked oauth/3rd party accounts for a member
    :param Member: The member to get the oauth accounts for
    :return: A list of oauth accounts
"""
def get_all_oauth_for_member(member):
    # -- Get the oauth model
    OAuth2 = apps.get_model('accounts.oAuth2')

    # -- Get all the oauth accounts
    oauth_accounts = OAuth2.objects.filter(user=member)

    return [account.serialize() for account in oauth_accounts]
