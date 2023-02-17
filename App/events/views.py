from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Event, EventReview
from .forms import (EventCreateForm, 
                    EventUpdateForm, 
                    EventDeleteForm, 
                    ReviewCreateForm, 
                    ReviewUpdateForm, 
                    ReviewDeleteForm)
import string
import random

                                        # **************
                                        # *** Events ***                                        # ***************
                                        # **************

# could be done with a class view, running the queries in
# get_context_objects, but currently I see no significant benefit
# in doing so.
def event_view(request, event_id):
    event = Event.objects.filter(event_id=event_id).first()
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

def event_update(request):
    context = {}

    form = EventUpdateForm(request.POST or None)
    if not request.user.is_streamer:
        return redirect('event_view')
    if form.is_valid():
        form.save()
        return redirect('event_view')

    context['form']= form
    return render(request, "event_edit.html", context)
        
def event_delete(request):
    context = {}

    form = EventDeleteForm(request.POST or None)
    if not request.user.is_streamer:
        return redirect('event_view')
    if form.is_valid():
        form.save()
        return redirect('all_events')

    context['form']= form
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
    if request.user.is_authenticated:
        request.user = get_user_model
    if form.is_valid():
        form.save()
        return redirect('event_view')

    context['form']= form
    return render(request, "review_new.html", context)

def review_update(request):
    context = {}

    form = ReviewUpdateForm(request.POST or None)
    if request.user.is_authenticated:
        request.user = get_user_model
    if form.is_valid():
        form.save()
        return redirect('event_view')

    context['form']= form
    return render(request, "review_edit.html", context)

def review_delete(request):
    context = {}

    form = ReviewDeleteForm(request.POST or None)
    if request.user.is_authenticated:
        request.user = get_user_model
    if form.is_valid():
        form.save()
        return redirect('event_view')

    context['form']= form
    return render(request, "review_delete.html", context)



EVENT_ID_CHARS = list(string.ascii_uppercase + string.ascii_lowercase + "1234567890")
EVENT_ID_LEN = 8

def generate_event_id():
    event_id = ""
    
    random

    for i in range(8):
        event_id += EVENT_ID_CHARS[random.randint(0, len(EVENT_ID_CHARS)-1)]

    return event_id


# class ReviewDetailView(DetailView):
#     model = EventReview
#     template_name = 'review_detail.html'

# class ReviewCreateView(CreateView):
#     model = EventReview
#     fields = ['title', 'body', 'rating']
#     template_name = 'review_new.html'
#     # success_url = reverse_lazy('view_event')

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.save()
#         return super().form_valid(form)

# class ReviewUpdateView(UpdateView):
#     model = EventReview
#     fields = ['title', 'body']
#     template_name = 'review_edit.html'

#     def form_valid(self, form):
#         form.instance.updated = timezone.now()
#         form.save()
#         return super().form_valid(form)

# class ReviewDeleteView(DeleteView):
#     model = EventReview
#     template_name = 'review_delete.html'
#     # success_url = reverse_lazy('all_events')

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.save()
#         return super().form_valid(form)
