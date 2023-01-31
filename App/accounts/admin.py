from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import MemberCreationForm, MemberChangeForm
from .models import Member, Streamer


# Register your models here.
class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    form = MemberChangeForm
    model = Member
    list_display = ['username','email','is_staff',]
    

admin.site.register(Member, MemberAdmin)
