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
    get_id_from_card,
    remove_stripe_payment_method,
    start_subscription_saved_payment,
    check_cust_payment_intent
)
import uuid


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
@required_data(["buyable_id", "payment_method"])
def create_payment_intent(request, data):

    # -- Get the users cars
    cards = get_cards_formatted(request.user)
    subscription = False

    # -- Create the payment intent 
    ids = data['buyable_id'].split(",")
    for i in range(len(ids)):
        if ids[i] == "ss_monthly" or ids[i] == "ss_yearly":
            subscription = True
            continue
        try: ids[i] = uuid.UUID(ids[i])
        except: return invalid_response("Invalid UUID")

    # -- Get the payment method
    payment_method = None


    # -- If the payment method is a dict, it's a new card
    #    otherwise it's a saved card
    if isinstance(data['payment_method'], dict):
        valid_entrys = ['card', 'exp_month', 'exp_year', 'cvc', 'name', 'save']
        for entry in valid_entrys:
            if entry not in data['payment_method']:
                return invalid_response("Invalid payment method, missing " + entry)
            
        # -- Add the payment method
        if (
            data['payment_method']['save'] is True or
            subscription is True
        ):
            payment_method = add_stripe_payment_method(
                request.user,
                data['payment_method']['card'],
                data['payment_method']['exp_month'],
                data['payment_method']['exp_year'],
                data['payment_method']['cvc'],
                data['payment_method']['name'],
            )

            # -- Check if the payment method is valid
            if payment_method[0] is None:
                return invalid_response(payment_method[1])
            
            payment_method = payment_method[0]["id"]


        # -- We are not saving the card, so we can just create
        #    a temporary payment method not linked to the user
        else: payment_method = get_id_from_card(
            data['payment_method']['card'],
            data['payment_method']['exp_month'],
            data['payment_method']['exp_year'],
            data['payment_method']['cvc'],
            data['payment_method']['name'],
        )
    
    # -- Check if the payment method is a saved card
    else:
        for card in cards:
            if card["id"] == data['payment_method']:
                payment_method = card["id"]
                break

    
    # -- Make sure the payment method is valid
    if payment_method is None:
        return invalid_response("Invalid payment method")

    # -- Create the payment intent
    response = create_cust_payment_intent(
        request.user, ids, payment_method
    )

    if response.get("error") is not None:
        return invalid_response(response.get("error"))
    
    # -- Return the payment intent
    return success_response("Intent created.", response)



@api_view(['POST'])
@impersonate()
@authenticated()
@required_data(['intent_id'])
def check_payment_intent(request, data):
    response = check_cust_payment_intent(request.user, data['intent_id'])
    
    if response.get("error"):
        return error_response(response["error"])
    
    match response["status"]:
        case "success": return success_response("Purchase completed!", {
            "status": "success",
            "purchase_id": response["purchase_id"]
        })
        case "cancelled": return error_response("Payment cancelled", {
            "status": "cancelled"
        })
        case "requires_action": return success_response("Additional action required.", {
            "next_action": response["next_action"],
            "status": "requires_action"
        })
    
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