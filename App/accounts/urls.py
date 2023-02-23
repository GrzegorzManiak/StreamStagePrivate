from django.urls import  path

from .email.views import (
    check_if_verified_recently_view,
    remove_key_view,
    resend_key_view,
    verify_key_view,
)
from .create.views import send_reg_verification
from .oauth import OAuthTypes, determine_app
from .profile.forms import change_basic_details
from .profile.views import profile, send_verification
from .views import get_token, login, logout, register, validate_token


urlpatterns = [
    # path('signup/', MemberSignUpView.as_view(), name='signup'),
    path('', profile, name='member_profile'),

    # -- Basic Auth
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),

    # -- Profile
    path('send_verification/', send_verification, name='send_verification'),
    path('edit/basic_details/', change_basic_details, name='edit_basic_details'),

    # -- Authentication
    path('token/', validate_token, name='token'),
    path('get_token/', get_token, name='get_token'),

    # -- OAuth2.0
    path('sso/google/', determine_app(OAuthTypes.GOOGLE), name='google'),
    path('sso/discord/', determine_app(OAuthTypes.DISCORD), name='discord'),
    path('sso/github/', determine_app(OAuthTypes.GITHUB), name='github'),


    # EMail Verification
    path('register/email', send_reg_verification, name='send_reg_verification'),

    path('email/remove/', remove_key_view, name='remove_key'),
    path('email/resend/', resend_key_view, name='resend_key'),
    path('email/verify/', verify_key_view, name='verify_key'),
    path('email/recent/', check_if_verified_recently_view, name='recent_key'),
]
