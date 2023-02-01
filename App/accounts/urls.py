from django.urls import path
from .views import MemberSignUpView

urlpatterns = [
    path('signup/', MemberSignUpView.as_view(), name='signup'),
]