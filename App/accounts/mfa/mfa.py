"""
    2FA

    Once a user request to setup MFA, a token will be generated
    and added to the below list with a reference to the user,
    the token will be valid for 15 minutes, after which it will
    be removed from the list.

    The user will then take the token and use it to setup MFA
    and they will be prompted to enter the token, if the token
    is valid, MFA will be setup for the user.

    If not, the user will be prompted to try again.


    {
        'user': <user>,
        'token': <token>,
        'time': <time>
    }
"""

# -- Imports
import pyotp
import time


temp_mfa_tokens = []



"""
    :name: check_duplicate
    :description: This function is used to check if the user
    :param user: The user to check
    
    :return: True if the user has a duplicate, False if not
"""
def check_duplicate(user) -> bool:
    for temp_token in temp_mfa_tokens:
        if str(temp_token['user']['id']) == str(user.id):
            return True
    return False



"""
    :name: delete_duplicate
    :description: This function is used to delete a duplicate
        token from the list
    :param user: The user to delete
"""
def delete_duplicate(user):
    for temp_token in temp_mfa_tokens:
        if temp_token['user'] == user:
            temp_mfa_tokens.remove(temp_token)
            return
    


"""
    :name: generate_token
    :description: This function is used to generate a token
        for the user to use to setup MFA
    :param user: The user to generate the token for
    :return: The token
"""
def generate_token(user) -> str:
    # -- Check if the user already has a token
    delete_duplicate(user)

    # -- Generate the token
    token = pyotp.random_base32()

    # -- Add the token to the list
    temp_mfa_tokens.append({
        'user': user,
        'token': token,
        'time': time.time()
    })

    # -- Return the token
    return token



"""
    :name: has_token
    :description: This function is used to check if the user
        has a token
    :param user: The user to check
    :return: True if the user has a token, False if not
"""
def has_token(user) -> bool:
    for temp_token in temp_mfa_tokens:
        if str(temp_token['user']['id']) == str(user.id):
            return True
    return False



"""
    :name: get_token
    :description: This function is used to get the token
        for the user
    :param user: The user to get the token for
    :return: list[str, str] - The token and a message
"""
def get_token(user) -> list[str, str]:
    for temp_token in temp_mfa_tokens:
        if temp_token['user'] == user:
            # -- Check if the token has expired
            if time.time() - temp_token['time'] > 900:
                temp_mfa_tokens.remove(temp_token)
                return [None, 'Sorry, but it seems like your token has expired, please try again']
            
            return [temp_token['token'], 'Congratulations, you have successfully generated a token']
        
    return [None, 'Sorry, but it seems like you do not have a token, please try again']



"""
    :name: verify_temp_otp
    :description: This function is used to verify the OTP
        that the user has entered
    :param user: The user to verify the OTP for
    :param otp: The OTP to verify
    :return: list[bool, str] - True if the OTP is valid, False if not
        and an explanation
"""
def verify_temp_otp(user, otp) -> list[bool, str]:

    token_data = get_token(user)
    if token_data[0] == None: return [False, token_data[1]]
    if not pyotp.TOTP(token_data[0]).verify(otp):
        return [False, 'Sorry, but it seems like the OTP you have entered is invalid, please try again']
    return [True, 'Congratulations, you have successfully verified your OTP']
