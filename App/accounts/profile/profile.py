"""
    This module contains contains functions
    to alter a user's profile.

    All functions will return a tuple containing
    a boolean and a string. The boolean will be
    True if the function was successful and False
    if it was not. The string will be a message
    describing the result of the function.
"""



# -- Imports
from django.utils.html import escape
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django_countries.fields import CountryField
from timezone_field import TimeZoneField

from accounts.email.verification import add_key, send_email
from accounts.create.create import email_taken, username_taken
from accounts.models import Member
from StreamStage.mail import send_template_email
from StreamStage.models import Statistics

from accounts.com_lib import model_to_dict

import secrets
import time



"""
    :name: validate_username
    :description: This is a username validator
        -- Must be between 3 and 20 characters
        -- Must Start with a letter
        def callback(data)
        -- Must not end with an underscore
        -- Must not contain spaces
    :param username: str - The username to validate
    :return: tuple[bool, str] - A tuple containing a bool
        which is True if the username is valid, False if it is not
        and a string which is the reason why it is not valid
"""
def validate_username(username) -> tuple[bool, str]:
    if len(username) < 3: return (False, 'Username is too short')
    if len(username) > 20: return (False, 'Username is too long')
    if not username[0].isalpha(): return (False, 'Username must start with a letter')
    if '__' in username: return (False, 'Username must not contain two underscores in a row')
    if username[-1] == '_': return (False, 'Username must not end with an underscore')
    if ' ' in username: return (False, 'Username must not contain spaces')

    return (True, 'Username is valid')



"""
    :name: change_username
    :description: This function changes a user's username   
        it ensurs that the username complies with the rules
        and that it is not already taken
    :param user: Member - The user to change the username for
    :param new_username: str - The new username
    :return: tuple[bool, str] - A tuple containing a bool
        which is True if the username was changed, False if it was not
        and a string which is the reason why it was not changed
"""
def change_username(user, new_username) -> tuple[bool, str]:
    # -- Check if the username is already taken
    if username_taken(new_username):
        # -- Find the user with the username
        user_with_username = Member.objects.get(username=new_username.lower())
        if user_with_username != user:
            return (False, 'Username is already taken')

    # -- Check that the username is different
    if user.username == new_username:
        return (True, 'Username is the same')

    # -- Check if the user is valid
    if not isinstance(user, Member):
        return (False, 'User is not valid')

    # -- Check if the username is valid
    validation = validate_username(new_username)
    if validation[0] == False:
        return validation

    # -- Change the username
    user.username = new_username.lower()
    user.cased_username = new_username
    user.save()

    return (True, 'Username changed successfully')



"""
    :name: change_description
    :description: This function changes a user's description
        it ensures that the description complies with the rules
        which ive no clue on what they are
    :param user: Member - The user to change the description for
    :param new_description: str - The new description
    :return: tuple[bool, str] - A tuple containing a bool
        which is True if the description was changed, False if it was not
        and a string which is the reason why it was not changed
"""
def change_description(user, new_description) -> tuple[bool, str]:
    # -- Check if the user is valid
    if not isinstance(user, Member):
        return (False, 'User is not valid')

    # -- Check if the description is valid
    if len(new_description) > 300:
        return (False, 'Description is too long')

    # -- Make sure the description is not the same
    if user.description == new_description:
        return (True, 'Description is the same')

    # -- Clean the description
    clean_description = escape(new_description)

    # -- Change the description
    user.description = clean_description
    user.save()

    return (True, 'Description changed successfully')



""" 
    :name: update_profile
    :description: This function updates a user's profile
        given a dictionary of data to update, it can update
        sensitive information by being provided with a
        validated_requests object (done by the view, not this function)
    :param user: Member - The user to update the profile for
    :param data: dict - A dictionary containing the data to update
    :param sensitive: bool - Whether or not to update sensitive information
    :return: tuple[bool, str] - A tuple containing a bool
        which is True if the profile was updated, False if it was not
        and a string which is the reason why it was not updated

    Object Structure:
    {
        # -- Basic Information
        'username': str,
        'description': str,
        'first_name': str,
        'last_name': str,
        'time_zone': str,
        'country': str,

        # -- Sensitive Information
        'tfa_token': str or None, # -- If None, then the user is not using 2FA / Unsets it
        'old_password': str,
        'password': str,
        'email': str,
    }
"""
def update_profile(user, data, sensitive=False) -> tuple[bool, str]:
    sensitive_fields = ['tfa_token', 'password', 'email']

    # -- Check if the user is valid
    if not isinstance(user, Member):
        return (False, 'User is not valid')
    
    # -- Check if the data is valid
    if not isinstance(data, dict):
        return (False, 'Data is not valid')
    
    # -- Check if the data is empty
    if len(data) == 0: return (False, 'Data is empty')

    # -- Check if the user is trying to update sensitive information
    if sensitive == False:
        for field in sensitive_fields:
            if field in data:
                return (False, 'User is not allowed to update sensitive information')
            

    # -- Update the username
    if 'username' in data:
        res = change_username(user, data['username'])
        if res[0] == False: return res

    # -- Update the description
    if 'description' in data:
        res = change_description(user, data['description'])
        if res[0] == False: return res

    # -- Update the first name
    if 'first_name' in data:
        user.first_name = data['first_name']

    # -- Update the last name
    if 'last_name' in data:
        user.last_name = data['last_name']

    # -- Update the time zone
    # NOTE: I have absolutely no idea why the time zone field
    # wont let me use the validate function, so i have to do this
    # abomination of a for loop
    if 'time_zone' in data:
        values = TimeZoneField().choices
        found = False

        for value in values:
            if value[1] == data['time_zone']:
                user.time_zone = data['time_zone']
                found = True
                break

        if found == False: return (False, 'Time zone is not valid')

    # -- Update the country
    if 'country' in data:
        try: CountryField().validate(model_instance=None, value=data['country'])
        except ValidationError: return (False, 'Country is not valid')
        user.country = data['country']

    # -- Update the 2FA token
    if 'tfa_token' in data:
        if data['tfa_token'] == None: user.tfa_token = None
        else: user.tfa_token = data['tfa_token']

    # -- Update the password
    if 'password' in data:
        if 'old_password' not in data:
            return (False, 'Old password is not provided')
        
        if not user.check_password(data['old_password']):
            return (False, 'Old password is incorrect')
        
        user.set_password(data['password'])
        if user.security_preferences.email_on_password_change:
            send_template_email(user, 'password_change')

    # -- Update the email
    if 'email' in data:
        try:
            validate_email(data['email'])
            user.email = data['email']

        except ValidationError:
            return (False, 'Email is not valid')


    # -- Get security preferences
    keys = user.security_preferences.get_keys()
    for key in keys:
        if key in data:
            user.security_preferences.set(key, data[key])

    # -- Save the user
    try: 
        user.save()
        return (True, 'Profile updated successfully')
    
    except Exception as e:
        return (False, str(e))
    


temporary_pats = []
PAT_EXPIRY_TIME = 60 * 15 # -- 15 minutes

"""
    :name: generate_pat
    :description: This function generates a new personal access token
        for a user, this allows the user to access sensitive information
        without having to provide their password
    :param user: Member - The user to generate the token for
    :param token: str - The token to use, optional
    :return: str - The generated token
"""
def generate_pat(user, token: str = None) -> str:
    user = model_to_dict(user)
    user = Member.objects.get(id=user['id'])
    
    # -- Check if the user is valid
    if not isinstance(user, Member):
        return None

    # -- Generate the token
    if token == None:
        token = secrets.token_urlsafe(32)

    # -- Add the token to the temporary list
    temporary_pats.append({
        'user': user,
        'token': token,
        'time': time.time()
    })

    return token



"""
    :name: get_pat
    :description: This function gets a personal access token
        from the temporary list
    :param token: str - The token to get
    :return: [dict, str] - A list containing a dict
        which is the token if it is found, None if it is not
        and a string which is the reason why it is not found
"""
def get_pat(token) -> list[dict, str]:
    # -- Check if the token is in the temporary list
    for pat in temporary_pats:
        if pat['token'] == token:

            # -- Check if the token has expired
            if time.time() - pat['time'] > PAT_EXPIRY_TIME:
                temporary_pats.remove(pat)
                return [None, 'Sorry, but it appears that the token has expired']
            
            return [pat, None]

    return [None, 'Sorry, but it appears that the token is not valid']



"""
    :name: validate_pat
    :description: This function validates a personal access token
        and returns the user that the token belongs to
    :param token: str - The token to validate
    :param member: Member - The member to validate the token for

    :return: list[bool, str] - A list containing a bool
        which is True if the token is valid, False if it is not
        and a string which is the reason why it is not valid
"""
def validate_pat(token, member) -> list[bool, str]:
    # -- Check if the token is in the temporary list
    pat_data = get_pat(token)
    if pat_data[0] == None:
        return [False, pat_data[1]]
    
    # -- Check if the token belongs to the member
    if pat_data[0]['user'] != member:
        return [False, 'Sorry, but it appears that the token does not belong to you']

    return [True, 'Congratulations, the token is valid']



"""
    :name: extend_pat
    :description: This function extends the expiry time of a personal access token
    :param token: str - The token to extend
    :param member: Member - The member to extend the token for
    :return: list[bool, str] - A list containing a bool
        which is True if the token is extended, False if it is not
        and a string which is the reason why it is not extended
"""
def extend_pat(token, member) -> list[bool, str]:
    # -- Check if the token is valid
    if not isinstance(token, str):
        return [False, 'Sorry, but it appears that the token is not valid']

    # -- Check if the member is valid
    if not isinstance(member, Member):
        return [False, 'Sorry, but it appears that the member is not valid']

    # -- Check if the token is in the temporary list
    pat_data = get_pat(token)
    if pat_data[0] == None:
        return [False, pat_data[1]]
    
    # -- Check if the token belongs to the member
    if pat_data[0]['user'] != member:
        return [False, 'Sorry, but it appears that the token does not belong to you']

    # -- Extend the token
    pat_data[0]['time'] = time.time()

    return [True, 'Token extended successfully']



"""
    :name: revoke_pat
    :description: This function revokes a personal access token
    :param token: str - The token to revoke
    :param member: Member - The member to revoke the token for
    :return: list[bool, str] - A list containing a bool
        which is True if the token is revoked, False if it is not
        and a string which is the reason why it is not revoked
"""
def revoke_pat(token, member) -> list[bool, str]:
    # -- Check if the token is valid
    if not isinstance(token, str):
        return [False, 'Sorry, but it appears that the token is not valid']

    # -- Check if the member is valid
    if not isinstance(member, Member):
        return [False, 'Sorry, but it appears that the member is not valid']

    # -- Check if the token is in the temporary list
    pat_data = get_pat(token)
    if pat_data[0] == None:
        return [False, pat_data[1]]
    
    # -- Check if the token belongs to the member
    if pat_data[0]['user'] != member:
        return [False, 'Sorry, but it appears that the token does not belong to you']

    # -- Revoke the token
    temporary_pats.remove(pat_data[0])

    return [True, 'Token revoked successfully']



"""
    :name: change_email
    :description: This function is responsible for changing the email
    :param member: Member - The member to change the email for
    :param new_email: str - The new email to change to
    :return: (string, string, string) - A tuple containing the new key
        or none if it failed, and a string which is the reason why it was not changed
"""
def change_email(
    member: Member,
    new_email: str,
) -> tuple[bool, str] or tuple[str, str, str]:
    new_email = new_email.lower()

    # -- Check if the email is already in use
    if email_taken(new_email): return (False, 'Email already in use')
    cur_email = member.email

    # -- Begin the transaction
    try:
        def callback(data):
            
            # -- Check if the email was taken
            if email_taken(new_email):
                raise Exception('Email already in use, Unlucky')
            
            # -- Check if the email was changed
            if member.email != cur_email:
                raise Exception('Email changed mid another email change')
            
            # -- Inform the user that the email was changed
            if member.security_preferences.email_on_email_change:
                send_template_email(member, 'email_change', {
                    'new_email': new_email,
                    'old_email': cur_email,
                })

            
            # -- Change the email
            Statistics.log('accounts', 'email_change')
            member.email = new_email.lower()
            member.save()

            
        keys = add_key(
            member,
            new_email,
            callback,
        )

        # -- Send the email
        res = send_email(keys[0])

        # -- Check if the email was sent
        if res[0] == False:
            return (False, res[1])

        # -- Return the keys
        return (keys[0], keys[1], keys[2])

    except Exception as e:
        return (False, 'An error occurred while trying to change the email')