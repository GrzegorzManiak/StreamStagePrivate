from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Member

class MemberCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Member
        fields = UserCreationForm.Meta.fields +('username', 'email',)

class MemberChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = UserCreationForm.Meta.fields 