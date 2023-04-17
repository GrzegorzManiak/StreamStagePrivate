# -- Imports
from rest_framework.decorators import api_view
from accounts.com_lib import authenticated, invalid_response, required_data, success_response, impersonate
from accounts.models import Member

@api_view(['GET'])
@impersonate()
@authenticated()
def get_subscription(request):
    # -- Return the subscription
    return success_response(
        'Subscription retrieved successfully', 
        request.user.serialize_subscription()
    )



@api_view(['POST'])
@impersonate()
@authenticated()
def cancel_subscription(request):
    # -- Check if the user has a subscription
    if request.user.subscription_status == 'none':
        return invalid_response('You do not have a subscription')
    
    # -- Cancel the subscription
    request.user.subscription_status = 'none'
    request.user.save()

    # -- Return the subscription
    return success_response('Subscription cancelled successfully')