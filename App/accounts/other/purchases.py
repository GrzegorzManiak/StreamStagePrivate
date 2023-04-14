from rest_framework.decorators import api_view
from accounts.com_lib import authenticated, invalid_response, required_data, success_response, paginate

from accounts.models import Member
from events.models import Event, EventReview
from orders.models import Purchase, PurchaseItem
from store.models import FlexibleTicket

@api_view(['GET'])
@authenticated()
@paginate(
    page_size=10,
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
   # validate=lambda request, model: model.user == request.user
)
def filter_purchases(request, models, total_pages, page):
    return success_response('Successfully filtered Purchases', {
        'purchases': [m.serialize() for m in models],
        'total_pages': total_pages,
        'page': page
    })