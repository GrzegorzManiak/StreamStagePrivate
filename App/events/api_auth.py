from accounts.com_lib import error_response
from functools import wraps
from django.shortcuts import redirect, render
from StreamStage.templatetags import cross_app_reverse

from .models import Event

def can_edit_event():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            
            # Not sure why data is only there sometimes.
            if hasattr(request, "data"): event_id = request.data.get('event_id')
            else: event_id = request.POST.get('event_id')
            if not event_id: event_id = kwargs.get("event_id")


            if request.method == 'POST':
                if not event_id:
                    return error_response("You must specify an event id for this resource.")
                event = Event.objects.filter(event_id = event_id).first()

                if not event:
                    return error_response("Invalid event ID specified.")
                
                if not request.user.is_authenticated:
                    return error_response("You do not have the permission to access this resource.")
                
            else:
                if not event_id: return redirect(
                    cross_app_reverse('homepage', 'homepage_index'))
                event = Event.objects.filter(event_id = event_id).first()

                if not event:
                    return redirect(cross_app_reverse('homepage', 'homepage_index'))
                
                if not request.user.is_authenticated:
                    return redirect(cross_app_reverse('accounts', 'login'))
                
                
            has_access = False
            if request.user.is_staff or request.user.is_superuser: has_access = True
            if event.broadcaster.streamer == request.user: has_access = True
            for contributor in event.broadcaster.contributors.all():
                if contributor == request.user: has_access = True

            if not has_access:
                return redirect(cross_app_reverse('homepage', 'homepage_index'))
            
            
            # -- Call the original function with the request object
            return view_func(request, event, *args, **kwargs)
        return wrapper
    return decorator