from django.urls import path, include
from .views import (
    validate_token,
    get_token,
    login,
    register,
    logout,
    profile
)

from .email.views import (
    recent_view,
    verify_view,
    resend_view,
    verify_view
)

urlpatterns = [
    # path('signup/', MemberSignUpView.as_view(), name='signup'),
    path('', profile, name='member_profile'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('verify/', verify_view, name='verify'),

    # -- Email
    path('email/recent/', recent_view, name='recent'),
    path('email/verify/', verify_view, name='verify'),
    path('email/resend/', resend_view, name='resend'),

    # -- Authentication
    path('token/', validate_token, name='token'),
    path('get_token/', get_token, name='get_token'),
    path('sso/', include('accounts.oauth.urls'), name='sso'),
]