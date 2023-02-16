from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Member, Broadcaster, oAuth2


# Register your models here.
class MemberAdmin(UserAdmin):
    model = Member
    list_display = ['username', 'email', 'is_staff', 'over_18', 'country', 'time_zone', 'max_keys', 'is_streamer']

class BroadcasterAdmin(admin. ModelAdmin):
    model = Broadcaster
    list_display = ['streamer', 'category']
    filter_horizontal = ['contributors']

class oAuth2Admin(admin.ModelAdmin):
    list_display = ['id', 'user', 'oauth_type', 'oauth_id']

admin.site.register(Member, MemberAdmin)
admin.site.register(Broadcaster, BroadcasterAdmin)
admin.site.register(oAuth2, oAuth2Admin)
