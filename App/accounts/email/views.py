from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view

from .verification import (
    check_if_verified_recently,
    get_key_by_resend_key,
    get_key,
    regenerate_key,
    remove_key,
    send_email,
    verify_key,
)


@api_view(['POST'])
def remove_key_view(request):
    key = request.data.get('token', None)

    if key is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Missing key',
        }, status=status.HTTP_400_BAD_REQUEST)

    res = remove_key(key)

    return JsonResponse({
        'status': res[0],
        'message': res[1],
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def verify_key_view(request):
    key = request.GET.get('token', None)

    res = verify_key(key)

        # -- Build the context
    context = {
        'verified': res[0],
        'message': res[1]
    }

    # -- Render the page
    return render(
        request, 
        'verify.html', 
        context=context
    )


@api_view(['POST'])
def resend_key_view(request):
    key = request.data.get('token', None)

    if key is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Missing key',
        }, status=status.HTTP_400_BAD_REQUEST)

    # -- Get the key data
    key_data = get_key_by_resend_key(key)

    # -- Check if they are allowed to change the email
    if key_data is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid key',
        }, status=status.HTTP_400_BAD_REQUEST)

    email = request.data.get('email', None)
    if email is not None and key_data['allow_email_change'] is True:
        key_data['user']['email'] = email

        # -- Check if we have a callback function
        if key_data['email_change_callback'] is not None:
            try: key_data['email_change_callback'](key_data['user'], email)
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Failed to change email',
                }, status=status.HTTP_400_BAD_REQUEST)

    res = regenerate_key(key)
    if res is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to regenerate key',
        }, status=status.HTTP_200_OK)

    res = send_email(res[0])
    return JsonResponse({
        'status': res[0],
        'message': res[1],
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def check_if_verified_recently_view(request):
    key = request.data.get('token', None)

    if key is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Missing key',
        }, status=status.HTTP_400_BAD_REQUEST)

    res = check_if_verified_recently(key)

    if res is False:
        return JsonResponse({
            'status': 'error',
            'message': 'Key not found',
        }, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({
        'status': 'success',
        'message': 'Key found',
    }, status=status.HTTP_200_OK)
    
