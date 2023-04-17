"""
    This file contains all the functions pertaining to payments.
    like saved cards, payment methods, Subscriptions, etc.
"""

# -- Imports
from typing import List
import uuid
from store.processing import on_intent_success, on_subscription_success
from store.processing import get_item_price
from StreamStage.mail import send_template_email
from accounts.models import Member
from StreamStage.secrets import STRIPE
import stripe

stripe.api_key = STRIPE['pri']
customer_payment_intents = {}



def clear_stripe_customer(user: Member):
    """
        :name: clear_stripe_customer
        :description: This function clears any incomplete payments for the user
        :param user: The user object
        :return: None
    """
    # -- Check if the user is valid
    if user is None: return None

    # -- Get the stripe customer
    customer = user.get_stripe_customer()

    # -- Check if the customer is valid
    if customer is None: return None

    # -- Get the payment intents
    payment_intents = stripe.PaymentIntent.list(
        customer=customer.id,
        limit=100,
    )

    # -- Loop through the payment intents
    # for payment_intent in payment_intents.data:
    #     # -- Cancel the payment intent
    #     stripe.Invoice.void_invoice(payment_intent.id)

    

def add_stripe_payment_method(
    user: Member,
    card: str,
    exp_month: int,
    exp_year: int,
    cvc: str,
    name: str,
) -> list:
    """
        :name: add_stripe_payment_method
        :description: This function adds a payment method to the user's stripe account
        :param user: The user object
        :param card: The card number
        :param exp_month: The expiration month
        :param exp_year: The expiration year
        :param cvc: The cvc code
        :return: a list, the first item being the payment method id, the second being
            a string dictating the error if there is one
    """
    # -- Check if the user is valid
    if user is None: return None

    # -- Get the stripe customer
    customer = user.get_stripe_customer()

    # -- Check if the customer is valid
    if customer is None: return None

    try: 
        # -- Create the payment method
        payment_method = stripe.PaymentMethod.create(
            type='card',
            card={
                'number': card,
                'exp_month': exp_month,
                'exp_year': exp_year,
                'cvc': cvc,
            },
        )

        # -- Attach the payment method to the customer
        stripe.PaymentMethod.attach(
            payment_method.id,
            customer=customer.id,
        )

        if user.security_preferences.email_on_payment_change:
            send_template_email(user, 'payment_method_added')

        return [
            format_payment_method(payment_method),
            'Payment method added successfully'
        ]
    
    except Exception as e:
        print(e)
        return [
            None,
            # Split on the first colon and return the second half
            str(e).split(':', 1)[1].strip()
        ]
    


def get_id_from_card(
    card: str,
    exp_month: int,
    exp_year: int,
    cvc: str,
    name: str,
) -> str:
    """
        :name: get_id_from_card
        :description: This function gets the payment method id from the card information
            Unlike the add_stripe_payment_method function, this function does not add the
            payment method to the user's stripe account
        :param card: The card number
        :param exp_month: The expiration month
        :param exp_year: The expiration year
        :param cvc: The cvc code
        :return: The payment method id
    """
    # -- Create the payment method
    try: 
        payment_method = stripe.PaymentMethod.create(
            type='card',
            card={
                'number': card,
                'exp_month': exp_month,
                'exp_year': exp_year,
                'cvc': cvc,
            },
        )

        return payment_method.id

    except Exception as e:
        print(e)
        return None



def get_stripe_payment_methods(user: Member):
    """
        :name: get_stripe_payment_methods
        :description: This function gets all the payment methods for the user
        :param user: The user object
        :return: The payment methods
    """
    # -- Check if the user is valid
    if user is None: return None

    # -- Get the stripe customer
    customer = user.get_stripe_customer()

    # -- Check if the customer is valid
    if customer is None: return None

    # -- Get the payment methods
    payment_methods = stripe.PaymentMethod.list(
        customer=customer.id,
        type='card',
    )

    return payment_methods



def format_payment_method(payment_method):
    """
        :name: format_payment_method
        :description: This function formats the payment method into a dictionary
        :param payment_method: The payment method object
        :return: The formatted payment method
    """
    # -- Check if the payment method is valid
    if payment_method is None: return None

    # -- Format the payment method
    payment_method_obj = {
        'id': payment_method.id,
        'brand': payment_method.card.brand,
        'last4': payment_method.card.last4,
        'exp_month': payment_method.card.exp_month,
        'exp_year': payment_method.card.exp_year,
        'created': payment_method.created,
    }

    return payment_method_obj



def get_cards_formatted(user: Member):
    """
        :name: get_cards_formatted
        :description: This function formats the payment methods into a list of cards
            with a limited amount of information
        :param user: The user object
    """
    # -- Get the payment methods
    payment_methods = get_stripe_payment_methods(user)
    if payment_methods is None: return None

    # -- Parse the payment methods
    return [format_payment_method(payment_method) for payment_method in payment_methods.data]



def remove_stripe_payment_method(user: Member, card_id: str):
    """
        :name: remove_stripe_payment_method
        :description: This function removes a payment method from the user's stripe account
        :param user: The user object
        :param card_id: The payment method id
        :return: True if the payment method was removed, False otherwise
    """
    # -- Check if the user is valid
    if user is None: return False

    # -- Get the stripe customer
    customer = user.get_stripe_customer()

    # -- Check if the customer is valid
    if customer is None: return False

    try:
        # -- Clear the stripe customer
        clear_stripe_customer(user)

        # -- Detach the payment method from the customer
        stripe.PaymentMethod.detach(
            payment_method=card_id,
        )

        # -- Email the user
        if user.security_preferences.email_on_payment_change:
            send_template_email(user, 'payment_method_removed')
            
        return True
    
    except Exception as e:
        print(e)
        return False
    


def create_stripe_payment_intent(
    user: Member, 
    amount: int | str, 
    payment_method: str,
    subscription: bool = False,
): 
    """
        :name: create_stripe_payment_intent
        :description: This function creates a payment intent for the user
        :param user: The user object
        :param amount: The amount to charge
        :param payment_method: The payment method id (optional)
        :return: The payment intent
    """
    # -- Check if the user is valid
    if user is None: return None
    customer = user.get_stripe_customer()

    # -- Create the payment intent
    if subscription == False:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='eur',
            customer=customer.id,
            payment_method_types=["card"],
            payment_method = payment_method
        )

    else:
        stripe.Customer.modify(
            customer.id,
            invoice_settings={ 'default_payment_method': payment_method },
        )

        payment_intent = stripe.Subscription.create(
            customer=customer.id,
            items=[{ 'price': amount }],
            expand=['latest_invoice.payment_intent'],
        )

    # -- Return the payment intent
    return payment_intent



def create_cust_payment_intent(user: Member, listing_ids: List[str], payment_method: str or dict):
    """
        Including a list of ticket listing ids, in the event that we decide we want
        the ability to buy more than one item at a time.

        Returns ID
    """
    price = 0
    subscription = False
    
    # -- If its ss_monthly, or ss_yearly we need to first check if they have a subscription
    #    and if so return an error.
    if listing_ids[0] == "ss_monthly" or listing_ids[0] == "ss_yearly":
        if user.is_subscribed(): return { "error": "You already have a subscription." }
        else: subscription = True

        if listing_ids[0] == "ss_monthly": price = STRIPE['prices']['ss_monthly']
        else: price = STRIPE['prices']['ss_yearly']

    

    # -- Get the price of each item
    for listing_id in listing_ids:
        if listing_id == "ss_monthly" or listing_id == "ss_yearly": continue
        item_price = get_item_price(listing_id)
        if item_price == None: return { "error": "Invalid listing ID given." }
        else: price += item_price

        
    # -- count how many cents are in price (Stripe only accepts integer val)
    try: 
        if subscription == False: price = int(price * 100)
        stripe_intent = create_stripe_payment_intent(user, price, payment_method, subscription)
    except Exception as e: return { "error": "Could not create intent, " + str(e) }
    
    # -- Try to instantly confirm the intent
    stripe_indent_id = None
    next_action = None
    if subscription == True: 
        formated_intent = format_subscription(stripe_intent)
        stripe_indent_id = formated_intent['id']
        
        na = stripe_intent['latest_invoice']['payment_intent']['next_action']
        if na["type"] == "redirect_to_url": next_action = na["redirect_to_url"]["url"]
        elif na["type"] == "use_stripe_sdk": next_action = na["use_stripe_sdk"]["stripe_js"]

    else: stripe_indent_id = stripe_intent['id']

    try: 
        if subscription == False: confirm_payment_intent(stripe_indent_id)
    except Exception as e: return { "error": "Could not confirm intent, " + str(e) }

    # -- Store the stripe intent masked behind our own id
    intent_id = str(uuid.uuid4())
    customer_payment_intents[intent_id] = {
        "user": user,
        "items": listing_ids,
        "stripe_intent": stripe_intent,
        "id": stripe_indent_id,
        "subscription": subscription,
        "payment_method": payment_method,
        "price": price,
        "next_action": next_action
    }

    # -- Return the external intent id
    return { "intent_id": intent_id }



def confirm_payment_intent(intent_id: str):
    """
        Attempts to confirm a stripe payment intent.
    """
    stripe.PaymentIntent.confirm(intent = intent_id)



def check_stripe_payment_intent_status(
    user: Member,
    cust_intent: dict,
):
    """
        Checks status of a stripe payment intent.
    """
    intent = cust_intent["stripe_intent"]
    intent.refresh()
    match intent["status"]:
        case "succeeded": 
            send_template_email(user, intent, 'payment_success')
            return { "status": "success" }
        
        case "canceled": 
            send_template_email(user, intent, 'payment_canceled')
            return { "status": "canceled" }
        
        case "active": 
            send_template_email(user, intent, 'subscription_success')
            return { "status": "success" }

        case "requires_payment_method": return { "status": "requires_payment_method" }
        case "requires_confirmation": pass
        case "incomplete":
            return { 
                "status": "requires_action",
                "next_action": cust_intent["next_action"]
            }
        
        case "requires_action":
            response = { "status": "requires_action" }
            next_action = intent["next_action"]

            if next_action["type"] == "redirect_to_url":
                response["next_action"] = next_action["redirect_to_url"]["url"]
            
            elif next_action["type"] == "use_stripe_sdk":
                response["next_action"] = next_action["use_stripe_sdk"]["stripe_js"]
            
            return response
        
    
    return { "status": "canceled" }



def check_cust_payment_intent(
    member: Member,
    intent_id: str
):
    cust_intent = customer_payment_intents.get(intent_id)

    if cust_intent is None:
        print("intent not found")
        return { "error": "Intent not found" }
    
    response = check_stripe_payment_intent_status(
        member,
        cust_intent
    )

    if response["status"] == "success":

        if cust_intent["subscription"] == True:
            purchase_id = on_subscription_success(cust_intent)
        else: purchase_id = on_intent_success(cust_intent)

        response["purchase_id"] = purchase_id

    return response




def start_subscription_saved_payment(user: Member, payment_method: str):
    """
        :name: start_subscription_saved_payment
        :description: This function starts a subscription for the user
        :param user: The user object
        :param payment_method: The payment method id
        :return: A list, the first being the subscription object, the second being
            the error if there is one
    """
    # -- Check if the user is valid
    if user is None: return False

    # -- Get the stripe customer
    customer = user.get_stripe_customer()

    # -- Check if the customer is valid
    if customer is None: return False

    try:
        # -- Clear the stripe customer
        clear_stripe_customer(user)

        # -- Attach the payment method to the customer
        stripe.PaymentMethod.attach(
            payment_method,
            customer=customer.id,
        )

        # -- Set the default payment method
        stripe.Customer.modify(
            customer.id,
            invoice_settings={
                'default_payment_method': payment_method,
            },
        )

        # -- Create the subscription
        sub = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                    'price': STRIPE['prices']['SSP'],
                },
            ],
            expand=['latest_invoice.payment_intent'],
        )

        return [
            format_subscription(sub),
            'Subscription started successfully'
        ]
    
    except Exception as e:
        print('Error: ' + str(e))
        return [
            None,
            # Split on the first colon and return the second half
            str(e)
        ]



def format_subscription(subscription):
    """
        :name: format_subscription
        :description: This function formats the subscription into a dictionary
        :param subscription: The subscription object
        :return: The formatted subscription
    """
    # -- Check if the subscription is valid
    if subscription is None: return None

    # -- Get the status
    status = subscription['status']

    # -- Format the subscription
    subscription_obj = {
        'id': subscription['id'],
        'start': subscription['current_period_start'],
        'end': subscription['current_period_end'],
        'created': subscription['created'],

        'invoice_id': subscription['latest_invoice']['id'],
        
        'payment_intent_id': subscription['latest_invoice']['payment_intent']['id'],
        'payment_intent_secret': subscription['latest_invoice']['payment_intent']['client_secret'],
    }

    if status != 'active':
        subscription_obj['requires_action'] = True
        subscription_obj['next_action'] = subscription['latest_invoice']['payment_intent']['next_action']

    else: subscription_obj['requires_action'] = False

    return subscription_obj