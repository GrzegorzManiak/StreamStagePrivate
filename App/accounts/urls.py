from django.urls import path, include
from .email import email_patterns
from .views import (
    validate_token,
    get_token,
    login,
    register,
    logout,
)

from .profile.views import (
    profile,
    send_verification
)
from .profile.forms import (
    change_basic_details,
)


urlpatterns = [
    # path('signup/', MemberSignUpView.as_view(), name='signup'),
    path('', profile, name='member_profile'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),

    path('email/', include(email_patterns), name='email'),

    path('send_verification/', send_verification, name='send_verification'),

    path('edit/basic_details/', change_basic_details, name='edit_basic_details'),

    # -- Authentication
    path('token/', validate_token, name='token'),
    path('get_token/', get_token, name='get_token'),
    path('sso/', include('accounts.oauth.urls'), name='sso'),
]