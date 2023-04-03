"""
    This contains the views for the payments functions
"""

# -- Imports
from rest_framework.decorators import api_view
from accounts.com_lib import authenticated, invalid_response, required_data, success_response, impersonate, error_response
from .payments import (
    add_stripe_payment_method,
    create_cust_payment_intent,
    get_cards_formatted,
    remove_stripe_payment_method,
    start_subscription_saved_payment,
    check_cust_payment_intent
)


@api_view(['POST'])
@authenticated()
@required_data(['card', 'exp_month', 'exp_year', 'cvc', 'name'])
def add_payment_method(request, data):
    # -- Add the payment method
    payment_method = add_stripe_payment_method(
        request.user,
        data['card'],
        data['exp_month'],
        data['exp_year'],
        data['cvc'],
        data['name'],
    )

    # -- Check if the payment method is valid
    if payment_method[0] is None:
        return invalid_response(payment_method[1])

    # -- Return the payment method
    return success_response(payment_method[1], payment_method[0])



@api_view(['GET'])
@impersonate()
@authenticated()
def get_payment_methods(request):
    # -- Get the payment methods
    payment_methods = get_cards_formatted(request.user)

    if payment_methods is None:
        return invalid_response('Could not retrieve payment methods')
    
    # -- Return the payment methods
    return success_response('Payment methods retrieved successfully', payment_methods)



@api_view(['POST'])
@impersonate()
@authenticated()
@required_data(['id'])
def remove_payment_method(request, data):
    # -- Remove the payment method
    payment_method = remove_stripe_payment_method(request.user, data['id'])

    if payment_method is False:
        return invalid_response('Could not remove payment method')

    # -- Return the payment method
    return success_response('Payment method removed successfully', payment_method)

@api_view(['POST'])
@authenticated()
@required_data(["ids"])
def create_payment_intent(request, data):
    ids = data["ids"]

    cards = get_cards_formatted(request.user)

    # -- Create the payment intent
    response = create_cust_payment_intent(request.user, ids, cards[0]["id"])

    if response.get("error") is not None:
        return invalid_response(response.get("error"))
    
    print(response.get("intent_id") + ", " + cards[0]["id"])
    # -- Return the payment intent
    return success_response("Intent created.", response)

@api_view(['POST'])
@impersonate()
@authenticated()
@required_data(['intent_id'])
def check_payment_intent(request, data):
    response = check_cust_payment_intent(data['intent_id'])
    
    if response.get("error"):
        return error_response(response["error"])
    
    status = response["status"]
    
    if status == "success":
        return success_response("Purchase completed!")
    elif status == "requires_action":
        data = { "next_action": response["next_action"] }

        return success_response("Additional action required.", data)
    elif status == "canceled":
        return error_response("Payment cancelled")
    
    return error_response("Error in checking status of payment")

@api_view(['POST'])
@impersonate()
@authenticated()
@required_data(['payment_method'])
def start_subscription(request, data):
    # -- Start the subscription
    subscription = start_subscription_saved_payment(request.user, data['payment_method'])

    if subscription[0] is None:
        return invalid_response(subscription[1])
    
    # -- Return the subscription
    return success_response('Subscription started successfully', subscription[0])