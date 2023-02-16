from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member, Broadcaster, oAuth2


# Register your models here.
@admin.register(Member)
class MemberAdmin(UserAdmin):
    model = Member
    list_display = ['username', 'email', 'is_staff', 'over_18', 'country', 'time_zone', 'max_keys', 'is_streamer']

@admin.register(Broadcaster)
class BroadcasterAdmin(admin. ModelAdmin):
    model = Broadcaster
    list_display = ['streamer', 'category', 'approved']
    filter_horizontal = ['contributors']

@admin.register(oAuth2)
class oAuth2Admin(admin.ModelAdmin):
    list_display = ['id', 'user', 'oauth_type', 'oauth_id']
