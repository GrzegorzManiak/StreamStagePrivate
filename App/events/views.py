from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import EventReview
from django.urls import reverse_lazy


class ReviewsDetailView(DetailView):
    model = EventReview
    template_name = 'review_detail.html'

class ReviewsListView(ListView):
    # *** CM
    # ***
    # Not sure if calling the right data & works for reviews of each event???
    queryset = EventReview.objects.filter(event='event').order_by('creation_date')
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