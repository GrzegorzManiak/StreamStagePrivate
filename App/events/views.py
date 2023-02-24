from django.shortcuts import render, redirect
import string, random
from .models import Event, EventReview, EventShowing
from .forms import (EventApplyForm, 
                    EventUpdateForm, 
                    EventDeleteForm, 
                    ReviewCreateForm, 
                    ReviewUpdateForm, 
                    ReviewDeleteForm,
                    ShowingCreateForm,
                    ShowingUpdateForm,
                    ShowingDeleteForm)

from . import inline_reviews


                                        # **************
                                        # *** Events ***                                        # ***************
                                        # **************

# Generating Event' s Random Event ID
EVENT_ID_CHARS = list(string.ascii_uppercase + string.ascii_lowercase + "1234567890")
EVENT_ID_LEN = 8

def generate_event_id():
    event_id = ""
    
    random

    for i in range(EVENT_ID_LEN):
        event_id += EVENT_ID_CHARS[random.randint(0, len(EVENT_ID_CHARS)-1)]

    return event_id

# could be done with a class view, running the queries in
# get_context_objects, but currently I see no significant benefit
# in doing so.
# Viewing an individual Event
def event_view(request, event_id):
    event = Event.objects.filter(event_id=event_id).first()

    if event == None:
        return redirect('all_events')
    
    reviews = event.get_reviews().order_by('-created')
    review_context = inline_reviews.handle(request, event)
    avg_rating = round(event.get_average_rating(reviews), 1)

    context = {
        'event': event, 
        'cover_pic': event.get_cover_picture(),
        'reviews' : reviews,
        'avg_rating': avg_rating,
        'new_review_form': review_context['new_review_form']
    }

    return render(request, 'event.html', context)

# Display All Events
def get_all_events(request):
    context = {}
    context["events"] = Event.objects.all()

    return render(request, "event_list.html", context)

def event_create(request):
    context = {}

    form = EventApplyForm(request.POST or None)
    if not request.user.is_authenticated or not request.user.is_streamer:
        return redirect('all_events')
    if form.is_valid():
        new_event_id = generate_event_id()
        form = form.save(commit=False)
        form.streamer = request.user
        form.event_id = new_event_id
        form.save()

        return redirect('event_view', new_event_id)

    context['form']= form
    return render(request, "event_new.html", context)

def event_update(request, event_id):
    context = {}
    event = Event.objects.get(event_id=event_id)

    if not request.user.is_authenticated or not request.user.is_streamer:
        return redirect('all_events')
    if event == None: # if event id in URL is invalid, redirect
        return redirect('all_events')
    
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
        return redirect('all_events')
    # if event id in URL is invalid or user doesn't own this event, redirect
    if event == None or not request.user == event.streamer:
        return redirect('all_events')
    
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
        form.save()
        # Adding the new showing to the event
        event.showings.add(form.save())

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
