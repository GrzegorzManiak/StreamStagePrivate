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
    update_profile_view, 
    remove_oauth, 
    extend_session,
    close_session,
    change_email_view,
    upload_image
)
from .mfa import (
    setup_mfa,
    verify_mfa,
    disable_mfa
)
from .payments.views import (
    add_payment_method,
    get_payment_methods,
    remove_payment_method,
    create_payment_intent,
    start_subscription
)

from .other import (
    get_reviews,
    update_review,
    delete_review
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
    path('api/update_profile/', update_profile_view, name='update_profile'),
    path('api/security/', security_info, name='security_info'),
    path('api/extend_session/', extend_session, name='extend_session'),
    path('api/close_session/', close_session, name='close_session'),
    path('api/change_img/', upload_image, name='change_pfp'),

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

    # -- Payments
    path('api/payment/methods/', get_payment_methods, name='get_payments'),
    path('api/payment/add/', add_payment_method, name='add_payment'),
    path('api/payment/remove/', remove_payment_method, name='remove_payment'),
    path('api/payment/create/', create_payment_intent, name='create_payment'),
    
    # -- Subscriptions
    path('api/subscription/start/', start_subscription, name='start_subscription'),
    
    # -- EMail Verification
    path('register/email', send_reg_verification, name='send_reg_verification'),

    path('api/email/remove/', remove_key_view, name='remove_key'),
    path('api/email/resend/', resend_key_view, name='resend_key'),
    path('email/verify/', verify_key_view, name='verify_key'),
    path('api/email/recent/', check_if_verified_recently_view, name='recent_key'),
    path('api/email/change/', change_email_view, name='change_email'),

    # -- Other
    path('api/other/get_reviews', get_reviews, name='get_reviews'),
    path('api/other/update_review', update_review, name='update_review'),
    path('api/other/delete_review', delete_review, name='delete_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
