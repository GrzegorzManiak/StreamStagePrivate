from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from accounts.com_lib import authenticated
from .api_auth import can_edit_event

from .models import EventShowing

from StreamStage.templatetags.tags import cross_app_reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Event, EventReview
from .forms import (EventUpdateForm, 
                    EventDeleteForm, 
                    ReviewCreateForm, 
                    ReviewUpdateForm, 
                    ReviewDeleteForm
                    )

from . import inline_reviews

from StreamStage import identifiers, secrets

                                        # **************
                                        # *** Events *** 
                                        # **************

# Viewing an individual Event
@csrf_exempt
def event_view(request, event_id):
    event = Event.objects.filter(event_id=event_id).first()

    if event == None:
        return redirect('upcoming_events')
    
    reviews = event.get_reviews().order_by('-created')
    review_context = inline_reviews.handle(request, event)
    avg_rating = round(event.get_average_rating(), 1)

    context = {
        'can_edit': event.is_authorized(request.user),
        'event': event,
        'cover_pic': event.get_cover_picture(),
        'reviews' : reviews,
        'avg_rating': avg_rating,
        'new_review_form': review_context['new_review_form'],
        
        'user': request.user,
        'api': {
            'send_verification': cross_app_reverse('accounts', 'send_verification'),
            'resend_verification': cross_app_reverse('accounts', 'resend_key'),
            'remove_verification': cross_app_reverse('accounts', 'remove_key'),
            'recent_verification': cross_app_reverse('accounts', 'recent_key'),

            'add_payment': cross_app_reverse('accounts', 'add_payment'),
            'get_payments': cross_app_reverse('accounts', 'get_payments'),
            'remove_payment': cross_app_reverse('accounts', 'remove_payment'),

            'create_payment': cross_app_reverse('accounts', 'create_payment'),
            'check_payment': cross_app_reverse('accounts', 'check_payment'),

            'get_reviews': cross_app_reverse('accounts', 'get_reviews'),
            'update_review': cross_app_reverse('accounts', 'update_review'),
            'delete_review': cross_app_reverse('accounts', 'delete_review'),
        },
        'stripe_key': secrets.STRIPE_PUB_KEY,
        'can_view': event.can_view(request.user) if request.user.is_authenticated else False,
    }

    return render(request, 'event.html', context)

# Display Past Events
@csrf_exempt
def get_past_events(request):
    context = {}
    context["events"] = [event for event in Event.objects.all() if event.can_view(request.user)
                         and event.get_showings_count() > 0 and event.get_num_upcoming_showings() == 0 
                         and event.approved]
    
    

    return render(request, "event_list_past.html", context)

# Display Live Events
@csrf_exempt
def get_live_events(request):
    context = {}
    evts = Event.objects.all()

    context["events"] = []
    for event in evts:
        if len(event.get_upcoming_showings()) > 0 and event.is_event_live() and event.approved:
            context["events"].append(event)

    return render(request, "event_list_live.html", context)

# Display Upcoming Events
@csrf_exempt
def get_upcoming_events(request):
    context = {}
    evts = Event.objects.all()
    
    context["events"] = []

    for event in evts:
        if len(event.get_upcoming_showings()) > 0 and event.approved:
            context["events"].append(event)

    return render(request, "event_list_upcoming.html", context)

# Update an event
@csrf_exempt
@authenticated()
@can_edit_event()
def event_update(request, event, event_id):

    context = {
        'event_id': event_id,

        'api': {
            'get_ticket_listings': cross_app_reverse('events', 'get_ticket_listings'),
            'add_ticket_listing': cross_app_reverse('events', 'add_ticket_listing'),
            'del_ticket_listing': cross_app_reverse('events', 'del_ticket_listing'),

            'get_showings': cross_app_reverse('events', 'get_showings'),
            'add_showing': cross_app_reverse('events', 'add_showing'),
            'del_showing': cross_app_reverse('events', 'del_showing'),

            'get_media': cross_app_reverse('events', 'get_media'),
            'add_media': cross_app_reverse('events', 'add_media'),
            'del_media': cross_app_reverse('events', 'del_media')
        }
    }
    
    form = EventUpdateForm(instance=event, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('event_view', event.event_id)
    else:
        form = EventUpdateForm(instance=event)
    
    context['form'] =  form
    return render(request, "event_update.html", context)
        
@csrf_exempt
def event_delete(request, event_id):
    context = {}
    event = Event.objects.get(event_id=event_id)
    
    if not request.user.is_authenticated or not request.user.is_streamer:
        return redirect('upcoming_events')
    # if event id in URL is invalid or user doesn't own this event, redirect
    if event == None or request.user != event.broadcaster.streamer:
        return redirect('upcoming_events')
    
    form = EventDeleteForm(instance=event)
    if request.POST:
        event.delete()
        return redirect('member_profile')
    else:
        form = EventDeleteForm(instance = event)
    
    context['form'] = form
    return render(request, "event_delete.html", context)


                                        # ***************
                                        # *** Reviews ***                                        # ***************
                                        # ***************
@csrf_exempt
def review_create(request):
    context = {}

    form = ReviewCreateForm(request.POST or None)
    if not request.user.is_authenticated:
        return redirect('event_view')
    if form.is_valid():
        form.save()
        return redirect('event_view')

    context['form']= form
    return render(request, "reviews/review_new.html", context)

@csrf_exempt
def review_update(request, event_id, review_id):
    review = EventReview.objects.filter(review_id=review_id).first()

    if not request.user.is_authenticated or not review.author == request.user:
        return redirect('event_view', event_id)
    
    form = ReviewUpdateForm(instance=review, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('event_view', event_id)
    else:
        form = ReviewUpdateForm(instance=review)

    context = {
        'form': form
    }

    return render(request, "reviews/review_update.html", context)

@csrf_exempt
def review_delete(request, event_id, review_id):
    review = EventReview.objects.filter(review_id=review_id).first()

    form = ReviewDeleteForm(instance=review)
    if not request.user.is_authenticated or review == None:
        return redirect('event_view', event_id)
    if request.POST:
        review.delete()
        return redirect('event_view', event_id)
    else:
        form = ReviewDeleteForm(instance = review)

    context = {
        'form': form,
        'review_obj': review
    }

    return render(request, "reviews/review_delete.html", context)

def reviews_view(request, event_id):
    context = {}
    context["event"] = Event.objects.filter(event_id=event_id).first()

    return render(request, "event_reviews.html", context)

def review_like(request, review_id):
    review = EventReview.objects.filter(review_id=review_id).first()
    review.toggle_like(request.user)
    return HttpResponse()

@authenticated()
def watch_event(request, showing_id):
    try:
        showing = EventShowing.objects.get(showing_id=showing_id)
        
        context = {
            showing: showing
        }
    except:
        showing = None

        context = {
            "error": "Showing not found."
        }
    

    

    # check if user is allowed to watch

    print(showing_id)

    return render(request, 'watch_event.html', context)