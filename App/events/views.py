from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Event, EventShowing, EventReview

# could be done with a class view, running the queries in
# get_context_objects, but currently I see no significant benefit
# in doing so.
def view_event(request, event_id):
    event = Event.objects.filter(event_id=event_id).first()
    
    primary_media_idx = event.primary_media_idx
    
    media = event.media.all()

    if media.count() == 0:
        cover_pic = None
    else:
        cover_pic = media[primary_media_idx]

    return render(request, 'event.html', {'event':event, 'cover_pic': cover_pic})



class ReviewsDetailView(DetailView):
    model = EventReview
    template_name = 'review_detail.html'

class ReviewsListView(ListView):
    # *** CM
    # ***
    # Not sure if calling the right data & works for reviews of each event???
    queryset = EventReview.objects.filter(event='event').order_by('created')
    template_name = 'reviews.html'
    context_object_name = "all_reviews_list"

class ReviewsCreateView(CreateView):
    model = EventReview
    fields = ['text']
    template_name = 'review_new.html'

class ReviewsUpdateView(UpdateView):
    model = EventReview
    fields = ['text']
    template_name = 'review_edit.html'

class ReviewsDeleteView(DeleteView):
    model = EventReview
    template_name = 'review_delete.html'
    success_url = reverse_lazy('event.html')