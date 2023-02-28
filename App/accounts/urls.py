from django.urls import  path

from .email.views import (
    check_if_verified_recently_view,
    remove_key_view,
    resend_key_view,
    verify_key_view,
)
from .create.views import send_reg_verification
from .oauth import OAuthTypes, determine_app
from .profile import (
    profile, 
    send_verification, 
    security_info, 
    update_profile, 
    remove_oauth, 
    extend_session,
)
from .mfa import (
    setup_mfa,
    verify_mfa,
    disable_mfa
)
from .views import get_token, login, logout, register, validate_token

from django.conf import settings
from django.conf.urls.static import static


# -- Should probably simplify this into GET/POST/PUT/DELETE instead of having multiple paths

urlpatterns = [
    # path('signup/', MemberSignUpView.as_view(), name='signup'),
    path('', profile, name='member_profile'),

    # -- Basic Auth
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),

    # -- Profile
    path('api/send_verification/', send_verification, name='send_verification'),
    path('api/update_profile/', update_profile, name='update_profile'),
    path('api/security/', security_info, name='security_info'),
    path('api/extend_session/', extend_session, name='extend_session'),

    # -- Authentication
    path('api/token/', validate_token, name='token'),
    path('api/get_token/', get_token, name='get_token'),
    path('api/mfa/setup', setup_mfa, name='setup_mfa'),
    path('api/mfa/verify', verify_mfa, name='verify_mfa'),
    path('api/mfa/disable', disable_mfa, name='disable_mfa'),

    # -- OAuth2.0
    path('sso/google/', determine_app(OAuthTypes.GOOGLE), name='google'),
    path('sso/discord/', determine_app(OAuthTypes.DISCORD), name='discord'),
    path('sso/github/', determine_app(OAuthTypes.GITHUB), name='github'),
    path('api/sso/remove/', remove_oauth, name='remove_oauth'),


    # -- EMail Verification
    path('register/email', send_reg_verification, name='send_reg_verification'),

    path('api/email/remove/', remove_key_view, name='remove_key'),
    path('api/email/resend/', resend_key_view, name='resend_key'),
    path('api/email/verify/', verify_key_view, name='verify_key'),
    path('api/email/recent/', check_if_verified_recently_view, name='recent_key'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
