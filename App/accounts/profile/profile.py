"""
    This module contains contains functions
    to alter a user's profile.

    All functions will return a tuple containing
    a boolean and a string. The boolean will be
    True if the function was successful and False
    if it was not. The string will be a message
    describing the result of the function.
"""
from django.utils.html import escape
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django_countries.fields import CountryField
from timezone_field import TimeZoneField

from accounts.create.create import username_taken
from accounts.models import Member


"""
    :name: validate_username
    :description: This is a username validator
        -- Must be between 3 and 20 characters
        -- Must Start with a letter
        -- Must only contain letters, numbers, and underscores
        -- Must not contain two underscores in a row
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
        return (False, 'Username is already taken')

    # -- Check that the username is different
    if user.username == new_username:
        return (False, 'Username is the same')

    # -- Check if the user is valid
    if not isinstance(user, Member):
        return (False, 'User is not valid')

    # -- Check if the username is valid
    validation = validate_username(new_username)
    if validation[0] == False:
        return validation

    # -- Change the username
    user.username = new_username.lower()
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
        return (False, 'Description is the same')

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
        change_username(user, data['username'])

    # -- Update the description
    if 'description' in data:
        change_description(user, data['description'])

    # -- Update the first name
    if 'first_name' in data:
        user.first_name = data['first_name']

    # -- Update the last name
    if 'last_name' in data:
        user.last_name = data['last_name']

    # -- Update the time zone
    if 'time_zone' in data:
        if TimeZoneField.validate(data['time_zone']) == False:
            return (False, 'Time zone is not valid')
        user.time_zone = data['time_zone']

    # -- Update the country
    if 'country' in data:
        if CountryField.validate(data['country']) == False:
            return (False, 'Country is not valid')
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

    # -- Update the email
    if 'email' in data:
        try:
            validate_email(data['email'])
            user.email = data['email']

        except ValidationError:
            return (False, 'Email is not valid')


    # -- Save the user
    try: 
        user.save()
        return (True, 'Profile updated successfully')
    
    except Exception as e:
        return (False, str(e))
    


    