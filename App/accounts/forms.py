from django.forms import forms
from django.forms import Form

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Member, StreamerProfile

class MemberCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Member
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

class MemberChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'first_name', 'last_name')

# class StreamerProfileCreationForm(Form):
#     category = forms.CharField(label="Content Category", max_length=50, min_length=1)

#     class Meta:
#         fields = ('category')

# class MemberUpdateForm(Form):
#     class Meta:
#         fields = ('category')
