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
            
        return 0

