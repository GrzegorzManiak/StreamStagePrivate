from accounts.com_lib import error_response
from functools import wraps
from django.shortcuts import redirect
from StreamStage.templatetags import cross_app_reverse
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
                
                if not request.user.is_authenticated:
                    return error_response("You do not have the permission to access this resource.")
            else:
                if not broadcaster:
                    return redirect(cross_app_reverse('homepage', 'homepage_index'))
                
                if not request.user.is_authenticated:
                    return redirect(cross_app_reverse('accounts', 'login'))
                
               
            if not request.user.is_staff:
                is_contributor = broadcaster.contributors.filter(id=request.user.id).exists()

                if not broadcaster.streamer != request.user and not request.user.is_streamer and not is_contributor:
                    return redirect(cross_app_reverse('homepage', 'homepage_index'))
            
            # -- Call the original function with the request object
            return view_func(request, broadcaster, *args, **kwargs)
        return wrapper
    return decorator