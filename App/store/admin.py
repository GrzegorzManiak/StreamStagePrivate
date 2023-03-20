from django.contrib import admin
from .models import FlexibleTicket

# Register your models here.

@admin.register(FlexibleTicket)
class FlexibleTicketAdmin(admin.ModelAdmin):
    list_display = [ 'ticket_id', 'item', 'event', 'purchased_date', 'ticket_price', 'showing' ]
