from StreamStage import secrets
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
import requests
from .oauth import oAuthRespone

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
    def get_access_token(self) -> oAuthRespone:
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
                return oAuthRespone.REQUEST_ERROR

            else: 
                try: json_response = response.json()
                except: return oAuthRespone.JSON_ERROR
                
        except:
            return oAuthRespone.REQUEST_ERROR

        # -- Parse the data
        self.access_token = json_response['access_token']
        if self.access_token == None:
            return oAuthRespone.ERROR

        # -- Return success
        return oAuthRespone.SUCCESS



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
                return oAuthRespone.REQUEST_ERROR

            else:
                try: response = response.json()
                except: return oAuthRespone.JSON_ERROR

        except:
            return oAuthRespone.REQUEST_ERROR

        # -- Parse the data
        id = response['id']
        email = response['email']
        verified_email = response['verified_email']
        name = response['name']
        given_name = response['given_name']
        picture = response['picture']

        # -- Make sure the data is valid
        if id == None or email == None or verified_email == None or name == None or given_name == None:
            return oAuthRespone.ERROR

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
        return oAuthRespone.SUCCESS




"""
    View for the Google OAuth2 login
"""
@api_view(['GET'])
def google_sso(request):
    
    # -- Get the code from the request
    code = request.GET.get('code')

    if code == None:
        # -- TODO: Redirect the user to the login page
        return JsonResponse({'message': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)

    # -- Create a new Google object
    google = Google(code)

    # -- Get the access token
    res = google.get_access_token()
    if res != oAuthRespone.SUCCESS:
        return JsonResponse({'message': str(res)}, status=status.HTTP_400_BAD_REQUEST)

    # -- Get the user info
    res = google.get_userinfo()
    if res != oAuthRespone.SUCCESS:
        return JsonResponse({'message': str(res)}, status=status.HTTP_400_BAD_REQUEST)

    # -- Return success
    return JsonResponse({
        'message': 'Success',
        'user': google.user.serialize()
    }, status=status.HTTP_200_OK)
