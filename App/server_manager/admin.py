from django.contrib import admin
from .models import Publisher, Server, StreamAccess

# Register your models here.
admin.site.register(Publisher)
admin.site.register(Server)
admin.site.register(StreamAccess)
