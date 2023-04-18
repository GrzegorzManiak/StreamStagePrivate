from rest_framework.decorators import api_view
from accounts.com_lib import authenticated, invalid_response, required_data, success_response, paginate, impersonate

from accounts.models import Member
from events.models import Event, EventReview
from orders.models import Purchase, PurchaseItem
from store.models import FlexibleTicket

@api_view(['GET'])
@impersonate()
@authenticated()
@paginate(
    page_size=5,
    search_fields=[
        'purchase_timestamp', 
        'billingAddress1', 'billingCity', 
        'billingPostcode', 'billingCountry',
        'purchase_id', 'total_multiplier'
    ],
    order_fields=[
        'purchase_timestamp', 
        'billingAddress1', 'billingCity', 
        'billingPostcode', 'billingCountry',
        'purchase_id', 'total_multiplier'
    ],
    model=Purchase,
    
    # -- This lambda checks if the user is the owner of the purchase
    validate=lambda request, model: model.purchaser == request.user
)
def filter_purchases(request, models, total_pages, page):
    return success_response('Successfully filtered Purchases', {
        'purchases': [m.serialize() for m in models],
        'page': page,
        'per_page': 5,
        'total': len(models),
        'pages': total_pages,
    })



@api_view(['GET'])
@impersonate()
@authenticated()
@paginate(
    page_size=10,
    search_fields=[
        'ticket_id', 
        'purchase_id',
        'purchased_date',
        'item__item_name',
    ],
    order_fields=[
        'ticket_id', 
        'purchase_id',
        'purchased_date',
        'item__item_name',
    ],
    model=FlexibleTicket,
    
    # -- This lambda checks if the user is the owner of the purchase
    validate=lambda request, model: model.item.purchase.purchaser == request.user
)
def tickets(request, models, total_pages, page):
    return success_response('Successfully filtered Purchases', {
        'tickets': [m.serialize() for m in models],
        'total_pages': total_pages,
        'page': page
    })
