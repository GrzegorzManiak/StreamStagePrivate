from enum import Enum
from StreamStage.secrets import OAUTH_PROVIDERS


class OAuthRespone(Enum):
    SUCCESS = 0
    ERROR = 1
    INVALID = 2
    JSON_ERROR = 3
    REQUEST_ERROR = 4
    EXPIRED = 5
    REDIRECT = 6

    def __str__(self):
        return f"OAuthRespone({str(self.value)})"



"""
    A type for the types of oauth
    that are supported
"""
class OAuthTypes():
    # -- Google, maybe discord and github
    GOOGLE = 0
    DISCORD = 1
    GITHUB = 2

    # -- Django choices
    choices = (
        (GOOGLE, 'Google'),
        (DISCORD, 'Discord'),
        (GITHUB, 'Github')
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
                return OAUTH_PROVIDERS['google']['ttl']
            
            case OAuthTypes.GITHUB:
                return OAUTH_PROVIDERS['github']['ttl']

            case OAuthTypes.DISCORD:
                return OAUTH_PROVIDERS['discord']['ttl']
        return 0



class User():
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
        self.description = None

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
        
    def get_email(self):
        return self.email.lower()

    def get_is_verified(self):
        return self.verified_email

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id
    
    def get_picture(self):
        return self.picture