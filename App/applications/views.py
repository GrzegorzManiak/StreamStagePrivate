from django.shortcuts import render, redirect
from .forms import *

from .processing import submit_streamer_application, submit_event_application, submit_broadcaster_application, get_broadcaster_application, get_streamer_application

# Create your views here.

def apply_for_event(request):
    pass

# def broadcaster_apply(request):
#     user = request.user

#     if not user.is_authenticated:
#         return redirect("events:all_events")
#     if user.is_staff:
#         return redirect("landing")
#     if not user.is_streamer and GetStreamerApplication(user) is None:
#         return redirect("landing")
#     if GetBroadcasterApplication(user) is not None:
#         return redirect("landing")

def apply_broadcaster(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('all_events')
    # user must either have a streamer application submitted, or be a streamer
    # to apply for a broadcaster profile.
    if get_streamer_application(request.user) is None and not request.user.is_streamer:
        return redirect('all_events')
    
    print(request.POST)
    # if the skip button was pressed
    if request.POST.get('skip') is not None:
        return redirect('apply_event')
        
    form = BroadcasterAppForm(request.POST or None)
    
    if form.is_valid():
        submit_broadcaster_application(user, form.data)

        return redirect('apply_event') # temporary

    context = { 'form': form }
    
    return render(request, "apply_broadcaster.html", context)

def apply_streamer(request):
    user = request.user

    if not request.user.is_authenticated:# or request.user.is_streamer:
        return redirect('all_events')
    
    form = StreamerAppForm(request.POST or None)
    
    if form.is_valid():
        submit_streamer_application(user, form.data)

        return redirect('apply_broadcaster') # temporary

    context = { 'form': form }

    return render(request, "apply_streamer.html", context)

def apply_event(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('all_events')
    # user must either have a broadcaster application submitted, or be a streamer
    # to apply for an event.
    if get_streamer_application(request.user) is None and not request.user.is_streamer:
        return redirect('all_events')
    # if the skip button was pressed
    if request.POST.get('skip') is not None:
        return redirect('apply_event')
    
    user_broadcasters = Broadcaster.objects.filter(streamer=user).values_list('handle', flat=True)
    form = EventAppForm(request.POST or None, streamer=user)
    
    if form.is_valid():
        event = form.save() # allow form to create event
        
        submit_event_application(user, event)

        return redirect('landing') # temporary

    context = {
        'form': form,
        'has_broadcaster': user_broadcasters.count() > 0
    }
    
    return render(request, "apply_event.html", context)


def landing_url(request):
    user = request.user

    if True:
        context = {
            'streamer_form': StreamerAppForm(),
            'broadcaster_form': BroadcasterAppForm()
        }

        return render(request, "users/apply.html", context)

    if user.is_authenticated:
        if user.is_staff:
            return render(request, "admin/review.html")
        elif user.is_streamer:
            return render(request, "users/apply.html")


    return redirect('events:all_events')

