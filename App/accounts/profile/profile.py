"""
    This module contains contains functions
    to alter a user's profile.

    All functions will return a tuple containing
    a boolean and a string. The boolean will be
    True if the function was successful and False
    if it was not. The string will be a message
    describing the result of the function.
"""
from accounts.models import Member
from accounts.email.registration import username_taken
from django.utils.html import escape

"""
    This is a username validator
    -- Must be between 3 and 20 characters
    -- Must Start with a letter
    -- Must only contain letters, numbers, and underscores
    -- Must not contain two underscores in a row
    -- Must not end with an underscore
    -- Must not contain spaces
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
    This function is responsible for changing
    a user's username
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
    This function changes a user's description
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

