from django.contrib.auth.hashers import make_password
from django.http.response import JsonResponse
from rest_framework import status
from django.conf import settings
import time
import secrets

from accounts.oauth.oauth import get_oauth_data, link_oauth_account

from accounts.email.verification import send_email
from accounts.models import Member

# -- Email Module
from accounts.email.verification import (
    add_key,
)

"""
    This file contains all things related to the
    creation of a new account.
"""

temp_users = {}

"""
    This function is responsible for cleaning up
    the database checking if a specific user has
    been expired
"""
def username_taken(username) -> bool:
    for key in temp_users:
        if temp_users[key]['username'] == username:
            
            # -- Check if the username has expired
            if time.time() - temp_users[key]['created'] > settings.EMAIL_VERIFICATION_TTL:
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
            if time.time() - temp_users[key]['created'] > settings.EMAIL_VERIFICATION_TTL:
                del temp_users[key]
                return False

            return True

    # -- Check the database
    if Member.objects.filter(email=email).first() is not None:
        return True

    return False




"""
    Create a new account
    with an email and password
"""
def create_account_email(
    email: str,
    username: str,
    password: str,
):
    # -- Check if the user already has an account
    if email_taken(email):
        return JsonResponse({
            'status': 'error',
            'message': 'An account with that email already exists',
        }, status=status.HTTP_400_BAD_REQUEST)

    if username_taken(username):
        return JsonResponse({
            'status': 'error',
            'message': 'An account with that username already exists',
        }, status=status.HTTP_400_BAD_REQUEST)


    email = email.lower()
    username = username.lower()
   
    # -- Verify the email
    return send_email(email, password, username)



"""
    :name: start_email_verification
    :description: This function is responsible for
                  starting the email verification process,
                  It creates the keys and sets up a callback
                  to create the account once the user has
                  verified their email

    :param email: The email of the user
    :param password: The password of the user
    :param username: The username of the user
    :param oauth: OPTIONAL - The oauth key of the user

    :return: The generated key
"""
def start_email_verification(
    email: str,
    password: str,
    username: str,
    oauth: str = None,
): 
    email = email.lower()

    # -- This is the identifier for the temp user
    temp_user_key = secrets.token_urlsafe(32)

    # -- Create the callback
    def callback(user):
        # -- First, make sure the 
        #    user is not None
        if user is None: return

        # -- The user's email is verified
        #    so we can create the account
        member = Member.objects.create(
            username=username,
            email=user['email'].lower(),
            password=make_password(password),
        )

        # -- Create the account
        if oauth is not None:
            # -- Create an account with an oauth id
            # -- Remove the oauth id from the session
            link_oauth_account(member, oauth)
            
            

        else:
            # -- Create an account with an email and password
            create_account_email(email, username, password)

        # -- Attempt to remove the user from the temp_users
        try: del temp_users[key]
        except KeyError: pass

    def change_email_callback(user, new_email):
        # -- First, make sure the 
        #    user is not None
        if user is None or new_email is None: return

        # -- Check if its taken 
        if email_taken(new_email):
            raise Exception('Email is taken')

        # Find the user in the temp_users
        for key in temp_users:
            if temp_users[key]['email'] == email:
                # -- Update the email
                temp_users[key]['email'] = new_email.lower()
        
    # -- Create the key
    key = add_key(
        {
            'email': email.lower(),
            'password': password,
            'username': username,
            'oauth': oauth,
            'provided_oauth': oauth is not None,
        },
        callback,
        change_email_callback,
    )

    # -- Create the account
    temp_users[temp_user_key] = {
        'email': email,
        'password': password,
        'username': username,
        'created': time.time(),
        'oauth': oauth,
    }

    # -- Send the email
    res = send_email(key[0])

    if res == False:
        print('Failed to send email')
        raise Exception(res[1])

    return key