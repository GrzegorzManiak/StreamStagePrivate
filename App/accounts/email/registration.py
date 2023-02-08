"""
    This file contains procedures for sending emails
    eg like email verification, password reset, etc
"""

# -- Imports
from StreamStage.mail import send_email as sm
from accounts.oauth.oauth import link_oauth_account
from django.http.response import JsonResponse
from django.contrib.auth.hashers import make_password
from rest_framework import status
from ..models import Member
import secrets
import time

REMOVE_AFTER = 60 * 60 * 24 * 7

temp_users = {}
resend_keys = {}
recently_verified = []

"""
    This function is responsible for cleaning up
    the database checking if a specific user has
    been expired
"""
def username_taken(username) -> bool:
    for key in temp_users:
        if temp_users[key]['username'] == username:
            
            # -- Check if the username has expired
            if time.time() - temp_users[key]['created'] > REMOVE_AFTER:
                del temp_users[key]
                return False

            return True

    # -- Check the database
    if Member.objects.filter(username=username).first() is not None:
        return True

    return False
    

def email_taken(email) -> bool:
    for key in temp_users:
        if temp_users[key]['email'] == email:
            
            # -- Check if the email has expired
            if time.time() - temp_users[key]['created'] > REMOVE_AFTER:
                del temp_users[key]
                return False

            return True

    # -- Check the database
    if Member.objects.filter(email=email).first() is not None:
        return True

    return False

    

"""
    This function is responsible for verifying the email
    of the user and storing them in a temporary database
    until they are verified.
"""
def send_email(email, username, password, oauth_token=None):
    email = email.lower()
    username = username.lower()

    # -- Now, we need to check if the user is already
    #    in the process of verifying their email
    if email_taken(email):
        return JsonResponse({
            'status': 'error',
            'message': 'An account with that email already exists'
        }, status=status.HTTP_400_BAD_REQUEST)

    if username_taken(username):
        return JsonResponse({
            'status': 'error',
            'message': 'An account with that username already exists'
        }, status=status.HTTP_400_BAD_REQUEST)
    


    # -- Generate a key
    key = secrets.token_urlsafe(64)
    resend_key = secrets.token_urlsafe(64)
    verify_token = secrets.token_urlsafe(64)

    # -- Store the key in the temporary database
    temp_users[key] = {
        'email': email,
        'username': username,
        'password': password,
        'created': time.time(),
        'verify_token': verify_token,
        'resend_key': resend_key,
        'oauth_token': oauth_token,
    }
    

    # -- Store the key in the resend database
    #    with value of the key to verify
    resend_keys[resend_key] = {
        'key': key,
    }

    # -- Send the email
    try:
        sm(
            email,
            'Verify your email',
            f'Click on this link to verify your email: https://me.streamstage.co/email/reg/verify?token={key}'
        )

        return JsonResponse({
            'status': 'success',
            'token': resend_key,
            'verify_token': verify_token,
            'message': 'Email sent'
        }, status=status.HTTP_200_OK)


    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to send email'
        }, status=status.HTTP_400_BAD_REQUEST)



"""
    This function is responsible for resending the verification
    email to the user, and extending the time for the user
    to verify their email
"""
def resend(resend_key, new_email=None):
    # -- Check if the key is valid
    if resend_keys.get(resend_key) is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid key, please refresh the page'
        }, status=status.HTTP_400_BAD_REQUEST)

    email_verifcation_key = resend_keys[resend_key]['key']


    # -- Make sure that its been adelast 1 minute
    #    since the last time the user requested
    #    a resend
    if time.time() - temp_users[email_verifcation_key]['created'] < 60:
        return JsonResponse({
            'status': 'error',
            'message': 'Wait 1 minute before requesting another resend'
        }, status=status.HTTP_400_BAD_REQUEST)


    # -- Check if the user has provided an alternative email
    #    to send the verification email to
    if new_email is not None:
        # -- Make sure the email is not already in use
        if email_taken(new_email):
            return JsonResponse({
                'status': 'error',
                'message': 'An account with that email already exists'
            }, status=status.HTTP_306_RESERVED)

        # -- Change the email in the temp_users database
        temp_users[email_verifcation_key]['email'] = new_email.lower()


    # -- Clonse the temp user, and delete the old one
    new_resend_key = secrets.token_urlsafe(64)
    new_key = secrets.token_urlsafe(64)

    temp_users[new_key] = temp_users[email_verifcation_key]
    temp_users[new_key]['created'] = time.time()
    temp_users[new_key]['resend_key'] = new_resend_key

    del temp_users[email_verifcation_key]
    del resend_keys[resend_key]

    resend_keys[new_resend_key] = {
        'key': new_key,
    }


    # -- Send the email
    try:
        sm(
            temp_users[new_key]['email'],
            'Verify your email',
            f'Click on this link to verify your email: https://me.streamstage.co/email/reg/verify?token={new_key}'
        )

        return JsonResponse({
            'status': 'success',
            'token': new_resend_key,
            'message': 'Email sent'
        }, status=status.HTTP_200_OK)


    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to send email'
        }, status=status.HTTP_400_BAD_REQUEST)



"""
    This function is responsible for verifying the user's
    email and creating the account
"""
def verify(key):
    # -- Check if the key is valid
    if temp_users.get(key) is None:
        return (False, 'Invalid key, please refresh the page')


    # -- Check if the user has taken too long to verify their email
    if time.time() - temp_users[key]['created'] > REMOVE_AFTER:
        # -- Remove the user from the temporary database
        del temp_users[key]
        return (False, 'Verification timed out, please try again')


    # -- Create the account
    try:
        # -- Get the user's details
        email = temp_users[key]['email']
        username = temp_users[key]['username']
        password = temp_users[key]['password']

        # -- Remove the user from the temporary database
        token = temp_users[key]['verify_token']

        # -- Check if the user has an oauth token
        oauth_token = temp_users[key]['oauth_token']

        del resend_keys[temp_users[key]['resend_key']]
        del temp_users[key]
        
        try: 
            member = Member.objects.create(
                email=email,
                username=username,
                password=make_password(password),
            )

            # -- If there is a oauth token, link the account
            if oauth_token is not None:
                link = link_oauth_account(member, oauth_token)

                if link == False:
                    # -- Remove the account
                    member.delete()
                    return (False, 'Failed to link account')

            
            # -- Add the user to the recently verified database
            recently_verified.append(token)

            return (True, 'Account created, you can now return to your previous page')

        except Exception as e:
            return (False, 'Failed to create account')



    except Exception as e:
        return (False, 'Failed to fetch user details')



"""
    THis function is responsible for checking if the user
    has recently verified their email, so the client can
    redirect them to the login page
"""
def recent(verify_token):

    # -- Try find the key in the list
    if verify_token in recently_verified:
        # -- Remove the key from the list
        recently_verified.remove(verify_token)

        return JsonResponse({
            'status': 'success',
            'message': 'Verified'
        }, status=status.HTTP_200_OK)

    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid key'
        }, status=status.HTTP_404_NOT_FOUND)
