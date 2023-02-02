from django.urls import path
from .views import MemberSignUpView #, MemberProfileView

urlpatterns = [
    path('signup/', MemberSignUpView.as_view(), name='signup'),
    # path('profile/', MemberProfileView.as_view(), name='member_profile'),

]