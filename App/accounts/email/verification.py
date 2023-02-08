"""
    This file contains the code for sending the verification link
    to the user's email, it is more generalpurpose than the other
    files in this folder, as this will be used for things like 
    verifying the user before they can reset their password etc.
"""

# -- Imports
import secrets
import time

from StreamStage.mail import send_email as sm

from ..models import Member


REMOVE_AFTER = 60 * 60 * 24 * 7

"""
    This variable stores all the temporary keys
    [key] = {
        key: str
        user: Member
        created: int
        callback: Function
    }

    This is what the resend key store looks like
    [
        {
            resend_key: str         -- Key used to resend the verification email
            verification_key: str   -- Key used by the client to check if the email has been verified
            key: str                -- Key used to verify the email
        }
    ]
"""
temp_keys_store = {}
resend_keys = []
recently_verified = []


"""
    This function adds a new key to the store and returns
    a touple, the first item is the key, the second item
    is the resend key
"""
def add_key(
    user: Member, 
    callback, 
    email_change_callback = None,
    ttl = REMOVE_AFTER
) -> tuple[str, str, str]:
    # -- Create the keys
    key = secrets.token_urlsafe(32)
    resend_key = secrets.token_urlsafe(32)
    verify_key = secrets.token_urlsafe(32)

    # -- Add the key to the store
    temp_keys_store[key] = {
        'key': key,
        'user': user,
        'created': time.time(),
        'callback': callback,
        'email_change_callback': email_change_callback,
        'verify_key': verify_key,
        'ttl': ttl,
        'allow_email_change': email_change_callback is not None,
    }

    # -- Add the resend key to the resend key store
    resend_keys.append({
        'resend_key': resend_key,
        'verification_key': verify_key,
        'key': key,
    })

    return (key, resend_key, verify_key)



""" 
    This function gets the key from the store
    and returns it
"""
def get_key(key: str) -> dict:
    if key in temp_keys_store:
        return temp_keys_store[key]
    return None



"""
    This function expires the key
"""
def expire_key(key: str) -> bool:
    if key in temp_keys_store:
        temp_keys_store[key]['created'] = 0
        return True
    return False



"""
    This function gets the resend key from the store
    and returns it
"""
def get_key_by_resend_key(resend_key: str) -> dict:
    for i in range(len(resend_keys)):
        if resend_keys[i]['resend_key'] == resend_key:
            return get_key(resend_keys[i]['key'])
    return None



"""
    This function gets the resend key from the store
    by the actual key
"""
def get_resend_key_by_key(key: str) -> dict:
    for i in range(len(resend_keys)):
        if resend_keys[i]['key'] == key:
            return resend_keys[i]
    return None


"""
    This function removes the key from the store
"""
def remove_key(key: str) -> bool:
    if key in temp_keys_store:
        del temp_keys_store[key]
        
        # -- Loop through the resend keys and remove the key
        for i in range(len(resend_keys)):
            if resend_keys[i]['key'] == key:
                del resend_keys[i]
                break

        return True
    return False



"""
    This function is responsible for verifying the email
    code 
"""
def verify_key(key) -> tuple[bool, str]:
    # -- Get the key from the store
    key = get_key(key)

    # -- Check if the key is valid
    if key is None:
        return (False, 'Invalid key')

    # -- Check if the key has expired
    if time.time() - key['created'] > key['ttl']:
        remove_key(key['key'])
        return (False, 'expired')

    # -- Try to call the callback
    try:
        key['callback'](key['user'])

    except Exception as e:
        return (False, 'Failed to call callback')

    # -- Remove the key from the store
    recently_verified.append({
        'key': key['verify_key'],
        'created': time.time(),
        'ttl': key['ttl'],
    })
    remove_key(key['key'])
    return (True, 'Sick! You can now return to your previous page')



"""
    This function actually sends the email to the user
"""
def send_email(
    key: str, 
    test=False,
) -> tuple[bool, str]:
    # -- Attempt to get the key from the store
    key = get_key(key)

    # -- Check if the key is valid
    if key is None:
        return (False, 'Invalid key')

    # -- Create the message
    message = f""" Your link is https://me.streamstage.co/email/verify?token={key['key']}"""

    # -- Send the email
    if test: return (True, message)
    else: 
        try:
            sm(
                key['user']['email'],
                'Verification Link',
                message,
            )
            return (True, 'Email sent')

        except Exception as e:
            return (False, 'Failed to send email')

    

"""
    This function is responsible for regenerating the key
    Some key notes:
        - We will need to clone the old key store entry
        - We will need to add the new key to the store
        - We will need to remove the old key from the store
        - We'll have to update the resend key store
"""
def regenerate_key(
    resend_key: str,
    new_email: str = None,
) -> dict or None:
    # -- Get the key from the store
    key = get_key_by_resend_key(resend_key)

    # -- Check if the key is valid
    if key is None: return None

    # -- Make sure the key hasn't expired
    if time.time() - key['created'] > key['ttl']: return None

    # -- Add the new key to the store
    key['user'].email = new_email if new_email is not None else key['user'].email
    new_key = add_key(key['user'], key['callback'], key['ttl'])

    # -- Remove the old key from the store
    remove_key(key['key'])

    # -- Return the new key
    return new_key



"""
    This function is responsible for checking if the email
    has been verified recently
"""
def check_if_verified_recently(verify_key: str) -> bool:
    for i in range(len(recently_verified)):
        key = recently_verified[i]
        
        if recently_verified[i]['key'] == verify_key:
            if time.time() - recently_verified[i]['created'] < recently_verified[i]['ttl']:
                return True
            else:
                del recently_verified[i]
                break
    return False
