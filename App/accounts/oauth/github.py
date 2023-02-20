import requests

from StreamStage import secrets
from accounts.oauth.types import OAuthRespone


class GithubUser():
    def __init__(
        self,
        id: int,
        email: str,
        verified_email: bool,
        name: str,
        given_name: str,
        description: str = None,
        picture: str = None,
    ):
        self.id = id
        self.email = email
        self.verified_email = verified_email
        self.name = name
        self.given_name = given_name
        self.picture = picture
        self.description = description

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'email_verified': self.verified_email,
            'name': self.name,
            'given_name': self.given_name,
            'picture': self.picture,
            'description': self.description,
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


class Github():
    def __init__(self, code=None):
        self.url = self.format_url()
        self.code = code
        self.access_token = None
        self.user = None

    """
        Formats the URL for the Github OAuth2 login
    """
    def format_url(self):
        redirect_uri = secrets.OAUTH_PROVIDERS['github']['redirect_uri']
        client_id = secrets.OAUTH_PROVIDERS['github']['client_id']
        api = secrets.OAUTH_PROVIDERS['github']['api_url']
        scopes = secrets.OAUTH_PROVIDERS['github']['scopes']

        scopes = ','.join(scopes)

        return f'{api}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}&response_type=code'



    """
        Gets the access token from Github
    """
    def get_access_token(self) -> OAuthRespone:
        json_response = None

        try:
            # -- Get the client id and secret
            client_id = secrets.OAUTH_PROVIDERS['github']['client_id']
            secret = secrets.OAUTH_PROVIDERS['github']['secret']
            access_url = secrets.OAUTH_PROVIDERS['github']['access_url']

            # -- Get the code
            code = self.code

            # -- Format the request
            data = {
                'client_id': client_id,
                'client_secret': secret,
                'code': code,
                'redirect_uri': secrets.OAUTH_PROVIDERS['github']['redirect_uri'],
            }

            headers = {
                'Accept': 'application/json',
            }

            # -- Send the request
            response = requests.post(
                access_url, 
                data=data, 
                headers=headers
            )

            # -- Check the status code
            if response.status_code != 200:
                return OAuthRespone.REQUEST_ERROR

            else: 
                try: json_response = response.json()
                except: return OAuthRespone.JSON_ERROR
                
        except:
            return OAuthRespone.REQUEST_ERROR

        # -- Parse the data
        if 'access_token' not in json_response:
            return OAuthRespone.ERROR

        self.access_token = json_response['access_token']

        # -- Return success
        return OAuthRespone.SUCCESS


    """
        Gets the user info from Google
    """
    def get_userinfo(self) -> GithubUser:
        try:
            # -- Get the access token
            access_token = self.access_token
            api = secrets.OAUTH_PROVIDERS['github']['userinfo_url']
            
            # -- Format the request
            headers = {
                'Authorization': f'Bearer {access_token}',
            }

            # -- Send the request
            response = requests.get(api, headers=headers)

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
        github_id = response['id']
        email = response['email']
        verified_email = False
        description = response['bio']
        name = response['login']
        given_name = response['name']
        picture = response['avatar_url']

        # -- Make sure the data is valid
        if github_id == None or email == None or description == None or name == None or given_name == None:
            return OAuthRespone.ERROR

        # -- Create the user object
        self.user = GithubUser(
            github_id, 
            email,
            verified_email, 
            name, 
            given_name, 
            description,
            picture
        )

        # -- Return success
        return OAuthRespone.SUCCESS
