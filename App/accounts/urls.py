from django.urls import path, include
from .email import email_patterns
from .profile import profile_patterns
from .views import (
    validate_token,
    get_token,
    login,
    register,
    logout,
    profile
)

urlpatterns = [
    # path('signup/', MemberSignUpView.as_view(), name='signup'),
    path('', profile, name='member_profile'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),

    path('email/', include(email_patterns), name='email'),
    path('profile/', include(profile_patterns), name='profile'),

    # -- Authentication
    path('token/', validate_token, name='token'),
    path('get_token/', get_token, name='get_token'),
    path('sso/', include('accounts.oauth.urls'), name='sso'),
]