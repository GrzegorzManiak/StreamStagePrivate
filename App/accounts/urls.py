from django.urls import path
from .views import (
    MemberSignUpView,
    validate_token,
    get_token
)

urlpatterns = [
    path('signup/', MemberSignUpView.as_view(), name='signup'),
    # path('profile/', MemberProfileView.as_view(), name='member_profile'),

    # -- Authentication
    path('token/', validate_token, name='token'),
    path('get_token/', get_token, name='get_token'),
]