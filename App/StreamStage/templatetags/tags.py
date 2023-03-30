from django.urls import reverse, reverse_lazy
from django import template
from StreamStage.settings import RUNNING_ON_LOCALHOST, DOMAIN_NAME

def cross_app_reverse(app, view, kwargs=None, use_subdomain=True):
    """
        This function is used to reverse urls
        that are in other apps
    """

    subdomain = 'www.'
    conf = ''
    match app:
        case 'accounts': 
            subdomain = 'me.'
            conf = 'accounts.urls'

        case 'events': 
            subdomain = 'events.'
            conf = 'events.urls'

        case 'applications': 
            subdomain = 'applications.'
            conf = 'applications.urls'
        
        case 'search':
            subdomain = 'search.'
            conf = 'search.urls'

        case 'homepage':
            subdomain = ''
            conf = 'homepage.urls'


    if RUNNING_ON_LOCALHOST == True or use_subdomain == False:
        return f'/{app}{reverse(view, urlconf=conf, kwargs=kwargs)}'

    full_domain = f'{subdomain}{DOMAIN_NAME}'
    return f'https://{full_domain}{reverse(view, urlconf=conf, kwargs=kwargs)}'

# This is the template tag equivalent of cross_app_reverse
# It is used to reverse urls in templates
register = template.Library()

@register.simple_tag
def cross_app_reverse_tag(
    app, 
    view, 
    use_subdomain=True,
    **kwargs,
):
    return cross_app_reverse(
        app, view, 
        kwargs=kwargs,
        use_subdomain=use_subdomain
    )