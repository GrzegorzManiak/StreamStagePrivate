from django.contrib import admin
from .models import Publisher, Server, StreamAccess

# Register your models here.
admin.site.register(Publisher)
admin.site.register(StreamAccess)

class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mode', 'region', 'slug', 'rtmp_ip', 'rtmp_port', 'http_ip', 'http_port')
    list_filter = ('mode', 'region')
    search_fields = ('name', 'slug', 'rtmp_ip', 'http_ip')

admin.site.register(Server, ServerAdmin)
