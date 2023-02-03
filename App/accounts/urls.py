from django.urls import path, include
from .views import (
    MemberSignUpView,
    validate_token,
    get_token,
    login
)

urlpatterns = [
    path('signup/', MemberSignUpView.as_view(), name='signup'),
    path('/', MemberSignUpView.as_view(), name='member_profile'),

    path('auth/', login, name='login'),
    # -- This has a spot for a 'configuration' parameter
    # kwargs={'configuration': 'login'}
    path(r'auth/(?P<configuration>[\w-]+)/', login, name='login'),

    # -- Authentication
    path('token/', validate_token, name='token'),
    path('get_token/', get_token, name='get_token'),
    path('sso/', include('accounts.oauth.urls'), name='sso'),
]