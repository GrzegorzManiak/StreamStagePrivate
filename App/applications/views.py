from django.shortcuts import render, redirect
from StreamStage.templatetags.tags import cross_app_reverse
from .forms import *
from .models import STATUS_WAITING, STATUS_APPROVED, STATUS_REJECTED, status_friendly_list
from accounts.com_lib import authenticated, is_admin
from django.views.decorators.csrf import csrf_exempt

from .processing import (
    submit_streamer_application,
    submit_event_application,
    submit_broadcaster_application,
    
    get_broadcaster_applications,
    get_streamer_applications,
    get_event_applications,

    approve_streamer_application,
    reject_streamer_application,

    approve_broadcaster_application,
    reject_broadcaster_application,

    approve_event_application,
    reject_event_application
)
# User views


@csrf_exempt
@authenticated()
def apply_broadcaster(request):
    user = request.user

    # user must either have a streamer application submitted, or be a streamer
    # to apply for a broadcaster profile.
    if get_streamer_applications(request.user).count() == 0 and not request.user.is_streamer:
        return redirect(cross_app_reverse('applications', 'apply_streamer'))
    
    # if the skip button was pressed
    if request.POST.get('skip') is not None:
        return redirect(cross_app_reverse('applications', 'apply_event'))
        
    form = BroadcasterAppForm(request.POST or None)
    
    if form.is_valid():
        submit_broadcaster_application(user, form.data)
        return redirect(cross_app_reverse('applications', 'apply_event'))# temporary

    context = { 'form': form }
    return render(request, "apply_broadcaster.html", context)


@csrf_exempt
@authenticated()
def apply_streamer(request):
    user = request.user
    
    form = StreamerAppForm(request.POST or None)
    
    if form.is_valid():
        submit_streamer_application(user, form.data)
        return redirect(cross_app_reverse('applications', 'apply_broadcaster'))

    context = { 'form': form }
    return render(request, "apply_streamer.html", context)

@csrf_exempt
@authenticated()
def apply_event(request):
    user = request.user

    # user must either have a broadcaster application submitted, or be a streamer
    # to apply for an event.
    if get_streamer_applications(request.user).count() == 0 and not request.user.is_streamer:
        return redirect(cross_app_reverse('applications', 'apply_streamer'))
    
    # if the skip button was pressed
    if request.POST.get('skip') is not None:
        return redirect(cross_app_reverse('applications', 'landing'))
    
    user_broadcasters = Broadcaster.objects.filter(streamer=user).values_list('handle', flat=True)
    form = EventAppForm(request.POST or None, streamer=user)
    
    if form.is_valid():
        # Unchecked checkboxes do not get sent in POST requests.
        if 'is_18s' not in form.data.keys():
            form.cleaned_data['is_18s'] = False

        event = submit_event_application(user, form.cleaned_data)
        return redirect(cross_app_reverse('events', 'event_view', { "event_id": event.event_id })) # temporary

    context = {
        'form': form,
        'has_broadcaster': user_broadcasters.count() > 0
    }
    
    return render(request, "apply_event.html", context)

# Admin views
@csrf_exempt
@authenticated()
@is_admin()
def list_applications(request):
    streamer_apps = StreamerApplication.objects.filter(status=STATUS_WAITING).all()
    broadcaster_apps = BroadcasterApplication.objects.filter(status=STATUS_WAITING).all()
    event_apps = EventApplication.objects.filter(status=STATUS_WAITING).all()

    context = {
        'streamer_apps': streamer_apps,
        'broadcaster_apps': broadcaster_apps,
        'event_apps': event_apps
    }

    return render(request, "admin/applications.html", context)

@csrf_exempt
@authenticated()
@is_admin()
def review_streamer_application(request, id):
    application = StreamerApplication.objects.filter(application_id=id).first()

    user = request.user

    if application is None:
        return redirect('review_applications')

    if request.POST.get("reject") is not None:
        reject_streamer_application(application, user)
        return redirect('review_applications')
        
    elif request.POST.get("approve") is not None:
        approve_streamer_application(application, user)
        return redirect('review_applications')

    return render(request, "admin/review_streamer.html", { 'app' : application })

@csrf_exempt
@authenticated()
@is_admin()
def review_broadcaster_application(request, id):
    application = BroadcasterApplication.objects.filter(application_id=id).first()

    user = request.user

    if application is None:
        return redirect('review_applications')

    if request.POST.get("reject") is not None:
        reject_broadcaster_application(application, user)
        return redirect('review_applications')
        
    elif request.POST.get("approve") is not None:
        approve_broadcaster_application(application, user)
        return redirect('review_applications')

    return render(request, "admin/review_broadcaster.html", { 'app' : application })

@csrf_exempt
@authenticated()
@is_admin()
def review_event_application(request, id):
    application = EventApplication.objects.filter(application_id=id).first()

    user = request.user

    if application is None:
        return redirect('review_applications')

    if request.POST.get("reject") is not None:
        reject_event_application(application, user)
        return redirect('review_applications')
        
    elif request.POST.get("approve") is not None:
        approve_event_application(application, user)
        return redirect('review_applications')

    return render(request, "admin/review_event.html", { 'app' : application })

@csrf_exempt
@authenticated()
def landing_url(request):
    user = request.user

    if user.is_staff:
        return redirect('review_applications')
    else:
        return redirect('apply_streamer')

