from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Member

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Member
        fields = UserCreationForm.Meta.fields +('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = UserCreationForm.Meta.fields 