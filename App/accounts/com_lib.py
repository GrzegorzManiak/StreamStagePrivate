"""
    This library came about as a result of the unorganized
    fassion that the api was written in, with inconsistent
    naming conventions, a lack of documentation, different
    ways of sending data back etc.

    This library is my attempt to fix all of that, and
    make the api more consistent and easier to work with
    for me on the frontend, and for others who might
    want to work on the api in the future.
"""

# -- Imports
from django.http.response import JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework import status

from functools import wraps


"""
    :name: success_response
    :description: This function is used to return a success response
                  to the user
    :param message: The message to send back to the user
    :param data: The data to send back to the user

    :return: A JsonResponse with the message and data
"""
def success_response(message, data=None):
    # -- Create the response
    response = {
        'message': message,
        'status': 'success'
    }

    # -- Check if we have data
    if data is not None:
        response['data'] = data

    # -- Return the response
    return JsonResponse(response, status=status.HTTP_200_OK)
    


"""
    :name: error_response
    :description: This function is used to return an error response
                  to the user, but not a 'you messed up' error
                  like a wrong password, but an error like
                  'no token provided'
    :param message: The message to send back to the user
    :return: A JsonResponse with the message
"""
def error_response(message):
    # -- Create the response
    response = {
        'message': message,
        'status': 'error'
    }

    # -- Return the response
    return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)



"""
    :name: invalid_response
    :description: This function is used to return an invalid response
                  to the user, this is used when the user has done
                  a boo boo, like sending the wrong password
    :param message: The message to send back to the user
    :return: A JsonResponse with the message
"""
def invalid_response(message):
    # -- Create the response
    response = {
        'message': message,
        'status': 'invalid'
    }

    # -- Return the response
    return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)



"""
    :name: authenticated
    :description: This function is used to check if the user is
                  authenticated, if they are not, it will return
                  an error response
"""
def authenticated():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # -- If the method is GET, redirect to the login page
            if request.method == 'GET':

                if not request.user.is_authenticated:
                    return redirect('login')
            
            # -- Check if user is authenticated
            if not request.user.is_authenticated:
                return error_response('You are not logged in')
            
            # -- Call the original function with the request object
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator



""" 
    :name: not_authenticated
    :description: This function is used to check if the user is
                  authenticated, if they are, it will return
                  an error response
"""
def not_authenticated():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # -- Check if user is authenticated
            if request.user.is_authenticated:
                return error_response('You are already logged in')
            
            # -- Call the original function with the request object
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator



"""
    :name: required_data
    :description: This function is used to check if the user has
                  provided all of the required data accounting 
                  for the method that they are using
    :param required: A list of the required data
"""
def required_data(required):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # -- Check if the user has provided all of the required data
            not_provided = []
            data_object = {}

            for data in required:
                if data not in request.data:
                    not_provided.append(data)

                else: data_object[data] = request.data[data]

            # -- Check if we have any data that was not provided
            if len(not_provided) > 0:
                return invalid_response('You did not provide the following required fields: {}'.format(', '.join(not_provided)))
            
            
            # -- Call the original function with the request object
            return view_func(request, data_object, *args, **kwargs)
        return wrapper
    return decorator