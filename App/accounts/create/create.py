"""
    This file contains all things related to the
    creation of a new account.

    It also contains functions for creating 
    temporary accounts and uniqueness checks.
"""

from django.contrib.auth.hashers import make_password
from django.http.response import JsonResponse
from rest_framework import status
from django.conf import settings
import time
import secrets

from accounts.oauth.oauth import link_oauth_account, get_oauth_data
from accounts.email.verification import send_email
from accounts.models import Member
from accounts.email.verification import add_key

temp_users = {}

"""
    :name: username_taken
    :description: This function checks if a username
        exists in either the database or the temp_users.
    :param username: String - The username to check
    :return: Boolean - True if the username is taken
"""
def username_taken(username) -> bool:
    for key in temp_users:
        if temp_users[key]['cased_username'] == username.lower():
            
            # -- Check if the username has expired
            if time.time() - temp_users[key]['created'] > settings.EMAIL_VERIFICATION_TTL:
                del temp_users[key]
                return False

            return True

    # -- Check the database
    if Member.objects.filter(cased_username=username.lower()).first() is not None:
        return True

    return False
    


"""
    :name: email_taken
    :description: This function checks if an email
        exists in either the database or the temp_users.
    :param email: String - The email to check
    :return: Boolean - True if the email is taken
"""
def email_taken(email) -> bool:
    email = email.lower()

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
    :name: create_account_email
    :description: This function is responsible for
        creating a temporary account, it also sends
        out an email to the provided email address
        with a link to verify the email.
    :param email: String - The email of the user
    :param username: String - The username of the user
    :param password: String - The password of the user
    :return: JsonResponse - The response
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
            cased_username=username.lower(),
            email=temp_users[temp_user_key]['email'].lower(),
            password=make_password(password),
        )

        # -- Create the account
        if oauth is not None:
            # -- Get the OAuth Data
            oauth_data = get_oauth_data(oauth)

            # -- Add the profile picture
            member.add_profile_pic_from_url(oauth_data['data']['picture'])

            # -- Link the account
            link_oauth_account(member, oauth)

        # -- Attempt to remove the user from the temp_users
        try: del temp_users[temp_user_key]
        except KeyError: pass

    def change_email_callback(user, new_email):
        # -- First, make sure the 
        #    user is not None
        if user is None or new_email is None: return False

        # -- Check if its taken 
        if email_taken(new_email):
            return False

        # Find the user in the temp_users
        temp_users[temp_user_key]['email'] = new_email.lower()
        return True
        
    # -- Create the key
    key = add_key(
        {
            'email': email.lower(),
            'cased_username': username.lower(),
            'password': password,
            'username': username,
            'oauth': oauth,
            'provided_oauth': oauth is not None,
        },
        email.lower(),
        callback,
        change_email_callback,
    )

    # -- Create the account
    temp_users[temp_user_key] = {
        'email': email,
        'cased_username': username.lower(),
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