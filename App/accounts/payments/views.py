"""
    This contains the views for the payments functions
"""

# -- Imports
from rest_framework.decorators import api_view
from accounts.com_lib import authenticated, invalid_response, required_data, success_response, impersonate
from .payments import (
    add_stripe_payment_method,
    get_cards_formatted,
    remove_stripe_payment_method,
    create_payment_intent,
    start_subscription_saved_payment
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
@impersonate()
@authenticated()
def create_payment_intent(request):
    # -- Create the payment intent
    payment_intent = create_payment_intent(request.user, 1000, 'pm_1MmVbfKeLSBX93CvGWW77Vgh')

    if payment_intent is None:
        return invalid_response('Could not create payment intent')

    # -- Return the payment intent
    return payment_intent



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