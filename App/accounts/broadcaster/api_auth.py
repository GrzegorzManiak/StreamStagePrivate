from accounts.com_lib import error_response
from functools import wraps
from django.shortcuts import redirect

from accounts.models import Broadcaster

def can_edit_broadcaster():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Not sure why data is only present sometimes.
            if hasattr(request, "data"):
                broadcaster_id = request.data.get('id')
            else:
                broadcaster_id = request.POST.get('id')

            if not broadcaster_id:
                broadcaster_id = kwargs.get("id")
            
            try: broadcaster = Broadcaster.objects.get(id=broadcaster_id)
            except Broadcaster.DoesNotExist:
                broadcaster = None

            if request.method == 'POST':
                if not broadcaster:
                    return error_response("Broadcaster not found.")

                if not broadcaster:
                    return error_response("Invalid event ID specified.")
                
                if not request.user.is_authenticated:
                    return error_response("You do not have the permission to access this resource.")
            else:
                if not broadcaster:
                    return redirect('homepage_index')
                
                if not request.user.is_authenticated:
                    return redirect('login')
                
               
            if not request.user.is_staff:
                if not request.user.is_streamer:
                    return redirect('homepage_index')

                if broadcaster.streamer != request.user and not broadcaster.contributors.filter(id=request.user.id).exists():
                    return redirect('homepage_index')
            
            # -- Call the original function with the request object
            return view_func(request, broadcaster, *args, **kwargs)
        return wrapper
    return decorator