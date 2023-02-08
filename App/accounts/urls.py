from django.urls import include, path

from .email.reg_views import recent_view, resend_view, verify_view
from .email.ver_views import (
    check_if_verified_recently_view,
    remove_key_view,
    resend_key_view,
    verify_key_view,
)
from .oauth.oauth import OAuthTypes, determine_app
from .profile.forms import change_basic_details
from .profile.views import profile, send_verification
from .views import get_token, login, logout, register, validate_token


# Profile MODULE

# OAuth2.0 MODULE

# Email Verification MODULE



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
    path('sso/google/', determine_app(OAuthTypes.GOOGLE), name='discord'),
    path('sso/google/', determine_app(OAuthTypes.GOOGLE), name='github'),


    # EMail Verification
    path('email/reg/recent/', recent_view, name='reg_recent'),
    path('email/reg/verify/', verify_view, name='reg_verify'),
    path('email/reg/resend/', resend_view, name='reg_resend'),
    path('email/reg/verify/', verify_view, name='reg_verify'),

    path('email/remove/', remove_key_view, name='remove_key'),
    path('email/resend/', resend_key_view, name='resend_key'),
    path('email/verify/', verify_key_view, name='verify_key'),
    path('email/recent/', check_if_verified_recently_view, name='recent_key'),
]
