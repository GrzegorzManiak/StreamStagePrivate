from StreamStage import secrets
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
import requests
from .oauth import (
    OAuthRespone, 
    generate_oauth_key,
    format_instructions,
    OAuthTypes,
)

class GoogleUser():
    def __init__(
        self,
        id: int,
        email: str,
        verified_email: bool,
        name: str,
        given_name: str,
        picture: str = None,
    ):
        self.id = id
        self.email = email
        self.verified_email = verified_email
        self.name = name
        self.given_name = given_name
        self.picture = picture

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'verified_email': self.verified_email,
            'name': self.name,
            'given_name': self.given_name,
            'picture': self.picture,
        }

    # 
    #  Getters,
    #  The reason for these is so that we can
    #  use the same functions on all oauth providers
    #  and some might have different names for the same
    #  data
    #
    def get_email(self):
        return self.email

    def get_is_verified(self):
        return self.verified_email

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id


class Google():
    def __init__(self, code=None):
        self.url = self.format_url()
        self.code = code
        self.access_token = None
        self.user = None

    """
        Formats the URL for the Google OAuth2 login
    """
    def format_url(self):
        redirect_uri = secrets.OAUTH_PROVIDERS['google']['redirect_uri']
        client_id = secrets.OAUTH_PROVIDERS['google']['client_id']

        return f'https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=openid%20email%20profile'    



    """
        Gets the access token from Google
    """
    def get_access_token(self) -> OAuthRespone:
        json_response = None

        try:
            # -- Get the client id and secret
            client_id = secrets.OAUTH_PROVIDERS['google']['client_id']
            secret = secrets.OAUTH_PROVIDERS['google']['secret']

            # -- Get the code
            code = self.code

            # -- Format the request
            url = 'https://oauth2.googleapis.com/token'
            data = {
                'code': code,
                'client_id': client_id,
                'client_secret': secret,
                'redirect_uri': 'https://sso.streamstage.co/google',
                'grant_type': 'authorization_code'
            }

            # -- Send the request
            response = requests.post(url, data=data)

            # -- Check the status code
            if response.status_code != 200:
                return OAuthRespone.REQUEST_ERROR

            else: 
                try: json_response = response.json()
                except: return OAuthRespone.JSON_ERROR
                
        except:
            return OAuthRespone.REQUEST_ERROR

        # -- Parse the data
        self.access_token = json_response['access_token']
        if self.access_token == None:
            return OAuthRespone.ERROR

        # -- Return success
        return OAuthRespone.SUCCESS



    """
        Gets the user info from Google
    """
    def get_userinfo(self) -> GoogleUser:
        try:
            # -- Get the access token
            access_token = self.access_token
            scope = secrets.OAUTH_PROVIDERS['google']['userinfo_url']

            # -- Format the request
            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            # -- Send the request
            response = requests.get(scope, headers=headers)

            # -- Check the status code
            if response.status_code != 200:
                return OAuthRespone.REQUEST_ERROR

            else:
                try: response = response.json()
                except: return OAuthRespone.JSON_ERROR

        except:
            return OAuthRespone.REQUEST_ERROR

        # -- Parse the data
        id = response['id']
        email = response['email']
        verified_email = response['verified_email']
        name = response['name']
        given_name = response['given_name']
        picture = response['picture']

        # -- Make sure the data is valid
        if id == None or email == None or verified_email == None or name == None or given_name == None:
            return OAuthRespone.ERROR

        # -- Create the user object
        self.user = GoogleUser(
            id, 
            email,
            verified_email, 
            name, 
            given_name, 
            picture
        )

        # -- Return success
        return OAuthRespone.SUCCESS




"""
    View for the Google OAuth2 login
    NOTE: This should probably be formatted to work with all
    OAuth2 providers
"""
@api_view(['GET'])
def google_sso(request):
    
    # -- Get the code from the request
    #    And if its none, just redirect
    #    The user to the oauth url
    code = request.GET.get('code')
    if code == None:
        return HttpResponseRedirect(Google().url)


    # -- Create a new Google object
    google = Google(code)

    # -- Get the access token
    res = google.get_access_token()
    if res != OAuthRespone.SUCCESS:
        return JsonResponse({'message': str(res)}, 
        status=status.HTTP_400_BAD_REQUEST)

    # -- Get the user info
    res = google.get_userinfo()
    if res != OAuthRespone.SUCCESS:
        return JsonResponse({'message': str(res)}, 
        status=status.HTTP_400_BAD_REQUEST)


    # -- Generate a reference key
    #    So that we can fetch this
    #    User later on
    key = generate_oauth_key(
        OAuthTypes.GOOGLE,
        google.user.serialize()
    )


    # -- Return success
    return JsonResponse({
        'message': 'Success',
        'user': google.user.serialize(),
        'token': key,
        'instructions': format_instructions(
            google.user.get_email(),
            google.user.get_is_verified(),
            OAuthTypes.GOOGLE,
            google.user.get_id()
        )
    }, status=status.HTTP_200_OK)
