from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from accounts.com_lib import authenticated
from .api_auth import can_edit_event

from StreamStage.templatetags.tags import cross_app_reverse

from .models import Event, EventReview, EventShowing
from .forms import (EventUpdateForm, 
                    EventDeleteForm, 
                    ReviewCreateForm, 
                    ReviewUpdateForm, 
                    ReviewDeleteForm,
                    ShowingCreateForm,
                    ShowingUpdateForm,
                    ShowingDeleteForm)

from . import inline_reviews

from StreamStage import identifiers, secrets

                                        # **************
                                        # *** Events *** 
                                        # **************

# Viewing an individual Event
def event_view(request, event_id):
    event = Event.objects.filter(event_id=event_id).first()

    if event == None:
        return redirect('upcoming_events')
    
    reviews = event.get_reviews().order_by('-created')
    review_context = inline_reviews.handle(request, event)
    avg_rating = round(event.get_average_rating(reviews), 1)

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
    }

    return render(request, 'event.html', context)

# Display Past Events
def get_past_events(request):
    context = {}
    context["events"] = Event.objects.all()

    return render(request, "event_list_past.html", context)

# Display Live Events
def get_live_events(request):
    context = {}
    context["events"] = Event.objects.all()

    return render(request, "event_list_live.html", context)

# Display Upcoming Events
def get_upcoming_events(request):
    context = {}
    context["events"] = Event.objects.all()

    return render(request, "event_list_upcoming.html", context)

# Update an event
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


                                        # ****************
                                        # *** Showings ***                                        # ***************
                                        # ****************
def showing_create(request, event_id):
    context = {}
    event = Event.objects.get(event_id=event_id)

    form = ShowingCreateForm(request.POST or None)
    if not request.user.is_authenticated or not request.user.is_streamer:
        return redirect('event_view', event_id)
    if form.is_valid():
        form = form.save(commit=False)
        form.streamer = request.user
        form.event = event
        form.save()

        return redirect('event_view', event_id)

    context['form']= form
    return render(request, "showings/showing_new.html", context)

def showing_update(request, event_id, showing_id):
    context = {}
    showing = EventShowing.objects.filter(showing_id=showing_id).first()

    if not request.user.is_authenticated or not request.user.is_streamer:
        return redirect('event_view', event_id)
    
    form = ShowingUpdateForm(instance=showing, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('event_view', event_id)
    else:
        form = ShowingUpdateForm(instance=showing)
    
    context['form'] =  form
    return render(request, "showings/showing_update.html", context)


def showing_delete(request, event_id, showing_id):
    showing = EventShowing.objects.filter(showing_id=showing_id).first()

    form = ShowingDeleteForm(instance=showing)
    if not request.user.is_authenticated or not request.user.is_streamer:
        return redirect('event_view', event_id)
    if showing == None:
        return redirect('event_view', event_id)
    if request.POST:
        showing.delete()
        return redirect('event_view', event_id)
    else:
        form = ShowingDeleteForm(instance = showing)

    context = {
        'form': form,
        'showing_obj': showing
    }

    return render(request, "reviews/review_delete.html", context)

                                        # ***************
                                        # *** Reviews ***                                        # ***************
                                        # ***************
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


def review_like(request, review_id):
    review = EventReview.objects.filter(review_id=review_id).first()
    review.toggle_like(request.user)
    return HttpResponse()


def watch_event(request, showing_id):
    try:
        showing = EventShowing.objects.get(showing_id=showing_id)
    except:
        showing = None

    context = {
        showing: showing
    }

    return render(request, 'watch_event.html', context)