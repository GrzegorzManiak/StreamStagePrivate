"""
    This file contains all the functions pertaining to payments.
    like saved cards, payment methods, Subscriptions, etc.
"""

# -- Imports
from accounts.models import Member
from StreamStage.secrets import STRIPE
import stripe

stripe.api_key = STRIPE['pri']



"""
    :name: clear_stripe_customer
    :description: This function clears any incomplete payments for the user
    :param user: The user object
    :return: None
"""
def clear_stripe_customer(user: Member):
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
def add_stripe_payment_method(
    user: Member,
    card: str,
    exp_month: int,
    exp_year: int,
    cvc: str,
    name: str,
) -> list:
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



"""
    :name: get_stripe_payment_methods
    :description: This function gets all the payment methods for the user
    :param user: The user object
    :return: The payment methods
"""
def get_stripe_payment_methods(user: Member):
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



"""
    :name: format_payment_method
    :description: This function formats the payment method into a dictionary
    :param payment_method: The payment method object
    :return: The formatted payment method
"""
def format_payment_method(payment_method):
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



"""
    :name: get_cards_formatted
    :description: This function formats the payment methods into a list of cards
        with a limited amount of information
    :param user: The user object
"""
def get_cards_formatted(user: Member):
    # -- Get the payment methods
    payment_methods = get_stripe_payment_methods(user)
    if payment_methods is None: return None

    # -- Parse the payment methods
    return [format_payment_method(payment_method) for payment_method in payment_methods.data]



"""
    :name: remove_stripe_payment_method
    :description: This function removes a payment method from the user's stripe account
    :param user: The user object
    :param card_id: The payment method id
    :return: True if the payment method was removed, False otherwise
"""
def remove_stripe_payment_method(user: Member, card_id: str):
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

        return True
    
    except Exception as e:
        print(e)
        return False
    


"""
    :name: create_payment_intent
    :description: This function creates a payment intent for the user
    :param user: The user object
    :param amount: The amount to charge
    :param payment_method: The payment method id (optional)
    :return: The payment intent
"""
def create_payment_intent(user: Member, ammount: int, payment_method: str = None): 
    # -- Check if the user is valid
    if user is None: return None
    customer = user.get_stripe_customer()

    # -- Create the payment intent
    payment_intent = stripe.PaymentIntent.create(
        amount=ammount,
        currency='usd',
        customer=customer.id,
        payment_method=payment_method,
    )

    # -- Return the payment intent
    return payment_intent



"""
    :name: start_subscription_saved_payment
    :description: This function starts a subscription for the user
    :param user: The user object
    :param payment_method: The payment method id
    :return: A list, the first being the subscription object, the second being
        the error if there is one
"""
def start_subscription_saved_payment(user: Member, payment_method: str):
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


"""
    :name: format_subscription
    :description: This function formats the subscription into a dictionary
    :param subscription: The subscription object
    :return: The formatted subscription
"""
def format_subscription(subscription):
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