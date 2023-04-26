"""
    This library contains the functions to send out a 
    verification email to a user, it can be used to 
    verify an email or to change an email or to create
    an account.
"""

# -- Imports
import requests
import secrets
import time
from StreamStage.mail import send_template_email
from StreamStage.models import Statistics

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
    :name: add_key
    :description: This function adds a new key to the store
        NOTE: this key store is NOT persistent between restarts
    :param data: dict - The data to store
    :param email: str - The email to send the verification email to
    :param callback: Function - The callback to call once the user has verified their email
    :param email_change_callback: Function - The callback to call once the user has verified their email
    :param ttl: int - The time to live of the key
    :return: tuple[str, str, str] - The key, the resend key and the verification key
"""
def add_key(
    data: dict, 
    email: str,
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
        'data': data,
        'email': email,
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
    :name: get_key
    :description: This function gets the key from the store
        and returns it
    :param key: str - The key to get
    :return: dict - The key or None if it does not exist
"""
def get_key(key: str) -> dict:
    if key in temp_keys_store:
        return temp_keys_store[key]
    return None


"""
    :name: expire_key
    :description: This function expires the key
        by just setting it 'created' to 0, so like
        1970 or something
    :param key: str - The key to expire
    :return: bool - True if the key was expired, False if it was not
        eg, if the key does not exist
"""
def expire_key(key: str) -> bool:
    if key in temp_keys_store:
        temp_keys_store[key]['created'] = 0
        return True
    return False



"""
    :name: get_key_by_resend_key
    :description: This function gets the key from the store
        by the resend key, used by the resend email endpoint
    :param resend_key: str - The resend key to get the key from
    :return: dict - The key or None if it does not exist
"""
def get_key_by_resend_key(resend_key: str) -> dict:
    for resend_key_obj in resend_keys:
        if resend_key_obj['resend_key'] == resend_key:
            return get_key(resend_key_obj['key'])
    return None



"""
    :name: get_resend_key_by_key
    :description: This function gets the resend key from the store
        by the key
    :param key: str - The key to get the resend key from
    :return: dict - The resend key or None if it does not exist
"""
def get_resend_key_by_key(key: str) -> dict:
    for i in range(len(resend_keys)):
        if resend_keys[i]['key'] == key:
            return resend_keys[i]
    return None



"""
    :name: remove_key
    :description: This function removes the key from the store
        It does it quite gracefully, it removes the key from 
        anything that it is in
    :param key: str - The key to remove
    :return: tuple[bool, str] - A tuple containing a bool
        which is True if the key was removed, False if it was not
        and a string which is the reason why it was not removed
"""
def remove_key(key: str) -> tuple[bool, str]:
    if key in temp_keys_store:
        del temp_keys_store[key]
        
        # -- Loop through the resend keys and remove the key
        for i in range(len(resend_keys)):
            if resend_keys[i]['key'] == key:
                del resend_keys[i]
                break

        return (True, 'The key was successfully terminated!')
    return (False, 'Sorry, but it appears that the key does not exist')



"""
    :name: verify_key
    :description: This function verifies the key
        and calls any callbacks that were provided
    :param key: str - The key to verify
    :return: tuple[bool, str] - A tuple containing a bool
        which is True if the key was verified, False if it was not
        and a string which is the reason why it was not verified
"""
def verify_key(key) -> tuple[bool, str]:
    # -- Get the key from the store
    key = get_key(key)

    # -- Check if the key is valid
    if key is None: return (False, 'Invalid key')

    # -- Check if the key has expired
    if time.time() - int(key['created']) > int(key['ttl']):
        remove_key(key['key'])
        return (False, 'expired')

    # -- Try to call the callback
    try: key['callback'](key['data'])
    except Exception as e:
        print(e)
        return (False, 'Failed to call callback')

    # -- Remove the key from the store
    recently_verified.append({
        'key': key['verify_key'],
        'created': time.time(),
        'ttl': REMOVE_AFTER,
    })
    remove_key(key['key'])
    return (True, 'Sick! You can now return to your previous page')



"""
    :name: send_email
    :description: This function sends the email
        I've abstracted it out so that you can use
        your own email service, we use SendGrid
    :param key: str - The key to send the email for
    :param test: bool - If this is True, it will not send the email
        but will return the message that would be sent
    :return: tuple[bool, str] - A tuple containing a bool
        which is True if the email was sent, False if it was not
        and a string which is the reason why it was not sent
"""
def send_email(
    key: str, 
    test=False,
) -> tuple[bool, str]:
    # -- Attempt to get the key from the store
    key = get_key(key)

    # -- Check if the key is valid
    if key is None: return (False, 'Invalid key')

    # -- Create the message
    message = f""" 
        URL: https://me.streamstage.co/email/verify?token={key['key']}
    """ 
    print(message)
    
    # NOTE: This is PURELY for testing purposes
    requests.get(f'https://me.streamstage.co/email/verify?token={key["key"]}')
    
    # -- Send the email
    if test: return (True, message)
    else: 
        try: 
            Statistics.log('accounts', 'mfa_email')
            send_template_email(
                key['email'],
                'verification',
                {
                    'url': f'https://me.streamstage.co/email/verify?token={key["key"]}',
                    'local': f'http://localhost:8000/accounts/email/verify?token={key["key"]}',
                }
            )
            return (True, 'Email sent')

        except Exception as e:
            return (False, f'Failed to send email: {e}')

    

"""
    :name: regenerate_key
    :description: This function is responsible for regenerating the key
        it will remove all references to the old key, making the old
        keys completely useless, which is a good thing.
    :param resend_key: str - The resend key to get the key from
    :param new_email: str - The new email to send the email to
    :return: tuple[bool, str, dict] - A tuple containing a bool
        which is True if the key was regenerated, False if it was not
        and a string which is the reason why it was not regenerated
        and a dict which is the new key.
"""
def regenerate_key(
    resend_key: str,
    new_email: str = None,
) -> dict or None:
    # -- Get the key from the store
    key = get_key_by_resend_key(resend_key)

    # -- Check if the key is valid
    if key is None: return [False, 'Invalid key', None]

    # -- Make sure the key hasn't expired
    if time.time() - key['created'] > key['ttl']:
        remove_key(key['key'])
        return [False, 'Key has expired', None]

    # -- Check if we are changing the email
    if (new_email is not None and key['allow_email_change'] is True): 
        # -- Check if we have a callback function
        if key['email_change_callback'] is not None:
            try: 
                should_continue = key['email_change_callback'](key['data'], new_email)
                if should_continue is False: return [False, 'Email already in use', None]
            except Exception as e: return [False, f'Failed to call email change callback: {e}', None]

        # -- Change the email
        key['email'] = new_email

    elif (new_email is not None and key['allow_email_change'] is False):
        return [False, 'Email change not allowed', None]

    # -- Generate a new key
    new_key = add_key(
        key['data'], 
        key['email'],
        key['callback'], 
        key['email_change_callback'],
        key['ttl'],
    )

    # -- Remove the old key from the store
    remove_key(key['key'])

    # -- Return the new key, or None if it failed
    if new_key is not None: return [True, 'Key regenerated', new_key]
    else: return [False, 'Failed to regenerate key', None]



"""
    :name: check_if_verified_recently
    :description: This function checks if the key has been verified
        when called it will check the recently_verified list, and if
        its there it will return true and remove the key from the list
    :param verify_key: str - The key to check
    :return: bool - True if the key has been verified recently, False if it has not
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
