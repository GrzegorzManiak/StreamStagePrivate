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
from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework import status
from django.test.client import RequestFactory

from functools import wraps
from django.contrib.auth import get_user_model
import secrets

from functools import reduce
from operator import or_
from django.db.models import Q

from StreamStage.templatetags.tags import cross_app_reverse

"""
    :name: model_to_dict
    :description: This function is used to convert a model  
    to a dict, this just standardizes the way we do it
"""
def model_to_dict(model):
    if model is None: return None
    if type(model) is dict: return model
    if hasattr(model, '__dict__'): return model.__dict__
    return model



"""
    :name: success_response
    :description: This function is used to return a success response
                  to the user
    :param message: The message to send back to the user
    :param data: The data to send back to the user

    :return: A JsonResponse with the message and data
"""
def success_response(message, data=None, status: int = 200):
    # -- Create the response
    response = {
        'message': message,
        'status': 'success'
    }

    # -- Check if we have data
    if data is not None:
        response['data'] = data

    # -- Return the response
    return JsonResponse(response, status=status)
    


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
    :param status: The code to send back to the user (optional)
    :return: A JsonResponse with the message
"""
def invalid_response(message, s = 400):
    # -- Create the response
    response = {
        'message': str(message),
        'status': 'invalid'
    }

    # -- Return the response
    return JsonResponse(response, status=s)



"""
    :name: api_session_helper
    :description: This decorator is used here in this file 
    internally, it is used to allow authenticated cross subdomain 
    requests to the api, when the user logs in, we assign them a
    token, this token is passed to us even if the session is not
"""
def api_session_helper():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # -- Check if the user is logged in 
            if request.user.is_authenticated:
                
                # -- Check if they passed a 'StreamStage-Token' header
                if 'streamstage-token' in request.headers:
                    # -- Check if it matches the token in the database
                    if request.headers['streamstage-token'] != request.user.token:
                        request.user.token = secrets.token_urlsafe(32)
                        request.user.save()

                # -- Check if they have a token
                elif request.user.token is None or request.user.token == '':
                    # -- Generate a token
                    request.user.token = secrets.token_urlsafe(32)
                    request.user.save()
                    
            # -- Check if we have a token and set the user
            if 'streamstage-token' in request.headers:
                # -- Get the user
                user = get_user_model().objects.filter(token=request.headers['streamstage-token']).first()

                # -- Check if we have a user
                if user is not None:
                    # -- Set the user
                    request.user = user
            
            # -- Call the original function with the request object
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator



"""
    :name: csrf_rewriter_middleware
    :description: This middleware is used to rewrite the csrf token
    from the x-csrftoken header to the cookie, this is used to allow
    authenticated cross subdomain requests to the api
"""
def csrf_rewriter_middleware(get_request):
    
    def middleware(request):
        # -- Get the request
        request = get_request(request)  
        # print(request.headers)

        # # -- Check for the 'ss-csrf-token' header
        # #    or 'x-csrftoken' header
        # if 'ss-csrf-token' in request.headers:
        #     # -- Set the cookie
        #     request.COOKIES['csrftoken'] = request.headers['ss-csrf-token']

        # # -- Check if we have a token
        # if 'x-csrftoken' in request.headers:
        #     # -- Set the cookie
        #     request.COOKIES['csrftoken'] = request.headers['x-csrftoken']

        # -- Return the request
        return request

    return middleware






"""
    :name: api_session_middleware
    :description: This middleware is used to set the 
    StreamStage-Token header on all requests, this is used
    to allow authenticated cross subdomain requests to the api,
"""
def api_session_middleware(get_response):
    
    def middleware(request):
        response = get_response(request)

        # -- Check for the 'StreamStage-Token' header
        if request.user.is_authenticated:
            # -- Add the header and cookie
            response.headers['streamstage-token'] = request.user.token
            response.set_cookie('streamstage-token', request.user.token)

        # -- Return the response
        return response

    return middleware


                
"""
    :name: authenticated
    :description: This function is used to check if the user is
                  authenticated, if they are not, it will return
                  an error response
"""
def authenticated():
    def decorator(view_func):
        @wraps(view_func)
        @api_session_helper()
        def wrapper(request, *args, **kwargs):

            # -- If the method is GET, redirect to the login page
            if request.method == 'GET' and not request.user.is_authenticated:
                return redirect(cross_app_reverse('accounts', 'login'))
            
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
            # -- If the method is GET, redirect to the login page
            if request.method == 'GET' and request.user.is_authenticated:
                return redirect(cross_app_reverse('accounts', 'member_profile'))
            
            # -- Check if user is authenticated
            if request.user.is_authenticated:
                return error_response('You are already logged in')
            
            # -- Call the original function with the request object
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator



"""
    :name: is_admin
    :description: This function is used to check if the user is
                    an admin, if they are not, it will return   
                    an error response
"""
def is_admin():
    def decorator(view_func):
        @wraps(view_func)
        @api_session_helper()
        def wrapper(request, *args, **kwargs):
            # If it is a GET request, Render a error page
            if request.method == 'GET' and not request.user.is_superuser:
                return render(request, 'error.html', {
                    'message': 'You do not have permission to do that'
                })
            
            # -- Check if user is an admin
            if not request.user.is_superuser:
                return error_response('You do not have permission to do that')
            
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

            if request.method == 'GET':
                for data in required:
                    if data not in request.GET:
                        not_provided.append(data)

                    else: data_object[data] = request.GET[data]
            
            else: 
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



"""
    :name: required_headers
    :description: This function is used to check if the user has
                    provided all of the required headers accounting 
                    for the method that they are using
    :param required: A list of the required headers
"""
def required_headers(required):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # -- Check if the user has provided all of the required data
            not_provided = []
            data_object = {}

            for data in required:
                if data not in request.headers:
                    not_provided.append(data)

                else: data_object[data] = request.headers[data]

            # -- Check if we have any data that was not provided
            if len(not_provided) > 0:
                return invalid_response('You did not provide the following required headers: {}'.format(', '.join(not_provided)))
            
            # -- Call the original function with the request object
            return view_func(request, data_object, *args, **kwargs)
        return wrapper
    return decorator




"""
    :name: impersonate
    :description: This function is used to impersonate a user
        so that we dont have to create a new set of API's to
        edit the user.

        To use this function, just have to pass in the ID of
        the user in the 'impersonate' header and it will
        automatically impersonate that user for any API calls

        This function will also check if the user is an admin
        and if they are not, it will do nothing.
"""
def impersonate():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # -- Check if the user is an admin
            if not request.user.is_superuser or not request.user.is_staff:
                request.impersonate = False
                return view_func(request, *args, **kwargs)
            
            user_id = None

            # -- Check if the user is trying to impersonate
            if 'impersonate' in request.headers:
                user_id = request.headers['impersonate']

            if request.method == 'GET' and 'impersonate' in request.GET:
                user_id = request.GET['impersonate']

            if user_id is None:
                request.impersonate = False
                return view_func(request, *args, **kwargs)

            try:
                # -- Save the original user
                request.impersonater = request.user

                # -- Get the user
                user = get_user_model().objects.get(id=user_id)

                # -- Make sure the uses is not an admin
                if user.is_superuser:
                    return invalid_response('You cannot impersonate an admin')

                # -- Set the impersonate flag to allow us to bypass some
                #    security checks
                request.user = user
                request.impersonate = True

            except Exception as e:
                print(e)
                request.impersonate = False
            
            # -- Call the original function with the request object
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator



"""
    :name: paginate
    :description: This decorator is used to create
    a basic pagination system for any model
"""
def paginate(
    order_fields: list,
    search_fields: list,
    page_size: int,
    model: object,

    # -- This lambda function is called to validate that the
    #    should be returned, we pass (request, model)
    validate: lambda request, model: bool = lambda request, model: True
):
    def decorator(view_func):

        @wraps(view_func)
        @required_data(['page', 'sort', 'order', 'search'])
        def wrapper(request, data, *args, **kwargs):
           
            # -- Make sure all the data is valid
            try: 
                page = int(data['page'])
                if page < 0: return invalid_response('Page must be greater than 0')
            except ValueError: return invalid_response('Page must be an integer')
            
            orders = ['asc', 'desc']
            if data['sort'] not in order_fields and data['sort'] != '':
                return invalid_response(f'Invalid sort field: {data["sort"]}, must be one of {", ".join(order_fields)}')
            if data['order'] not in orders: 
                return invalid_response(f'Invalid order: {data["order"]}, must be one of {", ".join(orders)}')

    
            sort = data['sort']
            if data['order'] == 'desc': sort = '-' + sort

            # -- Check if we are searching
            search = data['search'].strip().lower()
            query_list = [Q(**{f'{field}__icontains': search}) for field in search_fields]

            # -- Get the data
            models = model.objects.filter(reduce(or_, query_list))

            # -- Validate the data
            models = [model for model in models if validate(request, model)]

            # -- Get the page
            total_pages = int(len(models) / page_size)
            models = models[page * page_size:page * page_size + page_size]

            # -- Pass the models to the view
            return view_func(
                request, 
                models, 
                total_pages, 
                page,
                *args, 
                **kwargs
            )
        
        return wrapper
    return decorator


