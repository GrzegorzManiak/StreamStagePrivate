from django.shortcuts import render
from rest_framework.decorators import api_view

from accounts.com_lib import (
    required_data,
    required_headers,
    success_response,
    invalid_response,
)

from .verification import (
    check_if_verified_recently,
    get_key_by_resend_key,
    regenerate_key,
    remove_key,
    send_email,
    verify_key,
)


@api_view(['POST'])
@required_data(['token'])
def remove_key_view(request, data):
    """
        This view is used to remove a key
    """

    # -- Get the key data
    key_data = get_key_by_resend_key(data['token'])
    if key_data is None: return invalid_response('Invalid key')
    res = remove_key(key_data['key'])

    # -- Send the response
    if res[0] is False: return invalid_response(res[1])
    return success_response(res[1])



@api_view(['GET'])
@required_data(['token'])
def verify_key_view(request, data):
    """
        This view is used to verify a key,
        this is for the user.
    """

    res = verify_key(data['token'])
    print(res)
    return render(request, 'verify.html', 
        context= {
            'verified': res[0],
            'message': res[1]
        }
    )



@api_view(['POST'])
@required_data(['token'])
def resend_key_view(request, data):
    """
        This view is used to resend a verification email
        and to change the email to send to.
    """
    # -- Get the key data
    key_data = get_key_by_resend_key(data['token'])
    if key_data is None: return invalid_response('Invalid key')


    # -- Check if the user porivded an email to send to
    #    this is only used for account creation
    email = request.data.get('email', None)
    key_res = regenerate_key(data['token'], email)
    if key_res[0] is False: return invalid_response(key_res[1])


    # -- Send the email and return the response
    res = send_email(key_res[2][0])
    return success_response(res[1], {
        'token': key_res[2][1],
        'verify': key_res[2][2],
    })



@api_view(['POST'])
@required_data(['token'])
def check_if_verified_recently_view(request, data):
    """
        This view is used to check if a key has been verified
        recently (15 minutes)
    """
    if check_if_verified_recently(data['token']) is False:
        return invalid_response('Key not verified recently', 404)
    else: return success_response('Key verified recently')
