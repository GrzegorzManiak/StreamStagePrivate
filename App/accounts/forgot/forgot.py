from accounts.email.verification import add_key, send_email
from accounts.models import Member
from StreamStage.mail import send_template_email

import secrets
import time

temp_keys = [
    # {
    #     'member': Member,
    #     'key': str,
    #     'created': int,
    #     'expires': int,
    #     'cleared': bool
    # }
]


def request_password_reset(user: Member):
    """
        This function is used to request a password reset
        email
    """
    try:
        # -- Make sure the user is not none
        if user is None: return [ False, "User not found" ]


        # -- Check if the user has a key
        for key in temp_keys:
            if key['member'] == user:
                # -- Remove the key
                temp_keys.remove(key)


        # -- Generate a new key
        key = secrets.token_urlsafe(32)
        def callback(data):
            # -- Find the key
            clear_key = False
            for key in temp_keys:
                if (
                    key['member'] == user and 
                    key['key'] == data['key']
                ):
                    # -- Set the key to cleared
                    key['cleared'] = True
                    clear_key = True

            # -- Check if the key was found 
            if clear_key == False:
                raise Exception("Key not found")


        temp_keys.append({
            'member': user,
            'key': key,
            'created': time.time(),
            'expires': time.time() + 60 * 60,
            'cleared': False
        })
        keys = add_key(
            { 'member': user, 'key': key },
            user.email,
            callback,
        )
    

        # -- Send the email
        print(f'https://me.streamstage.co/email/verify?token={keys[0]}')
        send_template_email(
            user, "change_password",
            { "url": f'https://me.streamstage.co/email/verify?token={keys[0]}' }
        )

        # -- Return the keys
        return [key, keys[2], keys[1]]


    except Exception as e:
        return [False, 'An error occurred while trying to reset your password']
    


def verify_password_reset(key_in: str):
    """
        This function is used to verify a password reset
        key
    """
    try:
        # -- Check if the key is valid
        if key_in is None: return [False, "Invalid key"]

        # -- Find the key
        for key in temp_keys:
            if key['key'] == key_in:
                # -- Check if the key has expired
                if key['expires'] < time.time():
                    return [False, "Key has expired"]

                # -- Check if the key has been cleared
                if key['cleared'] == False:
                    return [False, "Key has not been cleared to perform this action"]

                # -- Check if the user is valid
                if key['member'] is None:
                    return [False, "User not found"]

                # -- Return the user
                return [True, key['member']]


        # -- Return the error
        return [False, "Key not found"]


    except Exception as e:
        return [False, 'An error occurred while trying to verify your password reset key']