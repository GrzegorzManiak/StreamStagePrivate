from django.contrib import admin
from .models import FlexibleTicket, Ticket

# Register your models here.

@admin.register(FlexibleTicket)
class FlexibleTicketAdmin(admin.ModelAdmin):
    list_display = [ 'valid_date_start', 'valid_date_end', 'ticket_id', 'event', 'showing', 'ticket_price', 'ticket_type' ]
    
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [ 'ticket_id', 'event', 'showing', 'ticket_price', 'ticket_type' ]
