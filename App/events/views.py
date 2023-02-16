from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Event, EventReview

                                        # **************
                                        # *** Events ***                                        # ***************
                                        # **************

# could be done with a class view, running the queries in
# get_context_objects, but currently I see no significant benefit
# in doing so.
def view_event(request, event_id):
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

class EventCreateView(CreateView):
    model = Event
    fields = ['event_id', 'title', 'description', 'categories', 'showings', 'media']
    template_name = 'event_new.html'
    success_url = reverse_lazy('view_event')

    def form_valid(self, form):
            form.instance.streamer = self.request.user
            form.save()
            return super().form_valid(form)

class EventUpdateView(UpdateView):
    model = Event
    fields = ['title', 'description', 'categories', 'showings', 'media']
    template_name = 'event_edit.html'
    success_url = reverse_lazy('view_event')

    def form_valid(self, form):
        form.instance.updated = timezone.now()
        form.save()
        return super().form_valid(form)

class EventDeleteView(DeleteView):
    model = EventReview
    template_name = 'review_delete.html'
    success_url = reverse_lazy('all_events')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


                                        # ***************
                                        # *** Reviews ***                                        # ***************
                                        # ***************

class ReviewDetailView(DetailView):
    model = EventReview
    template_name = 'review_detail.html'

# def get_all_reviews(request):
#     context = {}
#     context["reviews"] = EventReview.objects.filter(event=event)

#     for 
#     return render(request, "event_reviews_list.html", {
#         context,
#         'event': event})


class ReviewCreateView(CreateView):
    model = EventReview
    fields = ['title', 'body', 'rating']
    template_name = 'review_new.html'
    success_url = reverse_lazy('view_event')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

class ReviewUpdateView(UpdateView):
    model = EventReview
    fields = ['title', 'body']
    template_name = 'review_edit.html'

    def form_valid(self, form):
        form.instance.updated = timezone.now()
        form.save()
        return super().form_valid(form)

class ReviewDeleteView(DeleteView):
    model = EventReview
    template_name = 'review_delete.html'
    success_url = reverse_lazy('all_events')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)
