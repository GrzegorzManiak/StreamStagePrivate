from django.urls import path, include
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

    # -- Authentication
    path('token/', validate_token, name='token'),
    path('get_token/', get_token, name='get_token'),
    path('sso/', include('accounts.oauth.urls'), name='sso'),
]