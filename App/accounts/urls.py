from django.urls import path, include

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
    check_payment_intent,
    start_subscription
)

from .other import (
    get_reviews,
    update_review,
    delete_review,
    submit_report,
    users,
    get_user,
    delete_user,
    update_user_email,
    update_user_streamer
)
from .views import get_token, login, logout, register, validate_token

from .broadcaster.views import (
    edit_broadcasters,
    get_broadcaster_details,
    update_broadcaster_details
)

from django.conf import settings
from django.conf.urls.static import static

from .site import site_panel, get_statistics

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
    path('api/payment/check/', check_payment_intent, name='check_payment'),
    
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
    path('api/other/submit_report', submit_report, name='submit_report'),

    # -- Broadcaster
    path('broadcaster/', edit_broadcasters, name='edit_broadcasters'),
    path('broadcaster/get_details', get_broadcaster_details, name='get_broadcaster_details'),
    path('broadcaster/set_details', update_broadcaster_details, name='update_broadcaster_details'),

    # -- Admin
    path('site_panel/', site_panel, name='site_panel'),
    path('site_panel/get_statistics/', get_statistics, name='get_statistics'),
    path('site_panel/users/', users, name='users'),
    path('site_panel/get_user/', get_user, name='get_user'),
    path('site_panel/delete_user/', delete_user, name='delete_user'),
    path('site_panel/update_user_email/', update_user_email, name='update_user_email'),
    path('site_panel/update_streamer_status/', update_user_streamer, name='update_streamer_status'),

    path('events/', include('events.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
