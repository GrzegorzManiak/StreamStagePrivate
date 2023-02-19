from django.shortcuts import render, redirect
import string, random
from .models import Event, EventReview
from .forms import (EventCreateForm, 
                    EventUpdateForm, 
                    EventDeleteForm, 
                    ReviewCreateForm, 
                    ReviewUpdateForm, 
                    ReviewDeleteForm)


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

    reviews = EventReview.objects.filter(event=event).all()
    primary_media_idx = event.primary_media_idx
    
    media = event.media.all()

    if media.count() == 0:
        cover_pic = None
    else:
        cover_pic = media[primary_media_idx]

    return render(request, 'event.html', {
        'event': event, 
        'cover_pic': cover_pic,
        'reviews' : reviews
        })

# Display All Events
def get_all_events(request):
    context = {}
    context["events"] = Event.objects.all()

    return render(request, "event_list.html", context)

def event_create(request):
    context = {}

    form = EventCreateForm(request.POST or None)
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


                                        # ***************
                                        # *** Reviews ***                                        # ***************
                                        # ***************
# def get_all_reviews(request):
#     context = {}
#     context["reviews"] = EventReview.objects.filter(event=event)

#     for 
#     return render(request, "event_reviews_list.html", {
#         context,
#         'event': event})

def review_create(request):
    context = {}

    form = ReviewCreateForm(request.POST or None)
    if not request.user.is_authenticated:
        return redirect('event_view')
    if form.is_valid():
        form.save()
        return redirect('event_view')

    context['form']= form
    return render(request, "review_new.html", context)

def review_update(request):
    context = {}

    form = ReviewUpdateForm(request.POST or None)
    if not request.user.is_authenticated:
        return redirect('event_view')
    if form.is_valid():
        form.save()
        return redirect('event_view')

    context['form']= form
    return render(request, "review_update.html", context)

def review_delete(request, review_id):
    context = {}
    review = EventReview.objects.get(review_id=review_id)

    form = ReviewDeleteForm(instance=review)
    if not request.user.is_authenticated or review == None:
        return redirect('event_view')
    if request.POST:
        review.delete()
        return redirect('event_view')
    else:
        form = ReviewDeleteForm(instance = review)

    context['form']= form
    return render(request, "review_delete.html", context)
