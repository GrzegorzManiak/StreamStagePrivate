import requests
from StreamStage import secrets
from accounts.oauth.types import OAuthRespone, User

class Oauth():
    def __init__(self, code=None):
        self.url = self.format_url()
        self.code = code
        self.access_token = None
        self.user = None

    """
        Formats the URL for the Discord OAuth2 login
    """
    def format_url(self):
        redirect_uri = secrets.OAUTH_PROVIDERS['discord']['redirect_uri']
        client_id = secrets.OAUTH_PROVIDERS['discord']['client_id']
        api = secrets.OAUTH_PROVIDERS['discord']['api_url']
        scopes = secrets.OAUTH_PROVIDERS['discord']['scopes']
        scopes = '%20'.join(scopes)

        return f'{api}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scopes}'



    """
        Gets the access token from Discord
    """
    def get_access_token(self) -> OAuthRespone:
        json_response = None

        try:
            # -- Get the client id and secret
            client_id = secrets.OAUTH_PROVIDERS['discord']['client_id']
            secret = secrets.OAUTH_PROVIDERS['discord']['secret']

            # -- Get the code
            code = self.code

            # -- Format the request
            url = secrets.OAUTH_PROVIDERS['discord']['access_url']
            data = {
                'code': code,
                'client_id': client_id,
                'client_secret': secret,
                'redirect_uri': secrets.OAUTH_PROVIDERS['discord']['redirect_uri'],
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
    def get_userinfo(self) -> User:
        try:
            # -- Get the access token
            access_token = self.access_token
            scope = secrets.OAUTH_PROVIDERS['discord']['userinfo_url']

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
        print(response)
        # -- Parse the data
        discord_id = response['id']
        email = response['email']
        verified_email = response['verified']
        name = response['username']
        given_name = response['username']
        if response['display_name'] != None:
            given_name = response['display_name']
        picture = f'https://cdn.discordapp.com/avatars/{response["avatar"]}.png'

        # -- Make sure the data is valid
        if (
            discord_id == None or 
            email == None or 
            verified_email == None or 
            name == None or 
            given_name == None
        ):
            return OAuthRespone.ERROR

        # -- Create the user object
        self.user = User(
            discord_id, 
            email,
            verified_email, 
            name, 
            given_name, 
            picture
        )

        # -- Return success
        return OAuthRespone.SUCCESS
