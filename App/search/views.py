from events.models import Category, Event, EventShowing
from accounts.models import Broadcaster
from django.views.generic import ListView
from django.db.models import Q
from datetime import datetime
# from django.core.paginator import Paginator, EmptyPage, InvalidPage


class SearchResultsListView(ListView):
    model = Event
    context_object_name = 'events_list'
    template_name = 'search.html'
    # paginate_by = 8

    def get_queryset(self):
        user = self.request.user

        query = self.request.GET.get('q')
        sort = self.request.GET.get('s')
        category = self.request.GET.get('cat')
        broadcaster = self.request.GET.get('b')
        start_date = self.request.GET.get('sd')
        end_date = self.request.GET.get('ed')
        venue = self.request.GET.get('v')        
        city = self.request.GET.get('c')
        country = self.request.GET.get('co')
        # min_price = self.request.GET.get('mip')
        # max_price = self.request.GET.get('map')
        # purchased = self.request.GET.get('p')
        
        # Null Protection
        results = Event.objects.all()

        # Regular Search (User Input)
        if query:
            results = results.filter(Q(title__icontains=query) | Q(description__icontains=query))
        
        # Filter by Category
        if category:
            results = results.filter(Q(categories__name=category))
        
        # Filter by Broadcaster
        if broadcaster:
            print(broadcaster)
            results = results.filter(Q(broadcaster__handle__icontains=broadcaster))
            print(results)

        # Filter by Venue
        if venue:
            # Getting City from showings
            showings = EventShowing.objects.filter(venue=venue)
            # Matching Events to Showings
            events = []
            for showing in showings:
                events.append(showing.event)

            # Isolating event ID
            event_ids = []
            for event in events:
                event_ids.append(event.event_id)

            results = results.filter(event_id__in=event_ids)

        # Filter by City
        if city:
            # Getting City from showings
            showings = EventShowing.objects.filter(city=city)
            # Matching Events to Showings
            events = []
            for showing in showings:
                events.append(showing.event)

            # Isolating event ID
            event_ids = []
            for event in events:
                event_ids.append(event.event_id)

            results = results.filter(event_id__in=event_ids)

        # Filter by Country
        if country:
            # Getting Country from showings
            showings = EventShowing.objects.filter(country__name=country)
            # Matching Events to Showings
            events = []
            for showing in showings:
                events.append(showing.event)

            # Isolating event ID
            event_ids = []
            for event in events:
                event_ids.append(event.event_id)

            results = results.filter(event_id__in=event_ids)


        # Filter by Date
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
            end_date = datetime.strptime(end_date, '%d/%m/%Y').date()

            if not start_date:
                end_date = datetime.strptime(end_date, '%d/%m/%Y').date()
            
            # Getting Showings between dates
            showings = EventShowing.objects.filter(time__range=(start_date, end_date))
            # Matching Events to Showings
            events = []
            for showing in showings:
                events.append(showing.event)

            # Isolating event ID
            event_ids = []
            for event in events:
                event_ids.append(event.event_id)

            results = results.filter(event_id__in=event_ids)

        # # Filter by Price
        # # Ascending
        # if sort == 'price-asc':
        #     results = results.order_by('price')
        # # Descending
        # elif sort == 'price-desc':
        #     results = results.order_by('-price')
        
        # if min_price and max_price:
        #     min_price = int(min_price)
        #     max_price = int(max_price)

        #     if max_price == 0:
        #         max_price = 99999
            
        #     results = results.filter(price__range=(min_price, max_price))

        # Filter by Previous purchases
        # if purchased == 'y' and user.is_authenticated:
        #     valid_products = []

        #     orders = Order.objects.filter(registered_user=user)

        #     for order in orders:
        #         items = OrderItem.objects.filter(order=order)

        #         for item in items:
        #             valid_products.append(item.product)

        #     results = results.filter(name__in=valid_products)


        return results
    
    # If second search, keep original values
    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)

        # if you don't order_by brand first, distinct() doesn't seem to work.
        # context['brands'] = Event.objects.all().order_by('brand').values_list('brand', flat=True).distinct()

        context['is_search_page'] = True

        context['query'] = self.request.GET.get('q')
        context['sort_by'] = self.request.GET.get('s')
        context['category'] = self.request.GET.get('cat')
        context['categories'] = Category.objects.all()
        context['broadcaster'] = self.request.GET.get('b')
        context['start_date'] = self.request.GET.get('sd')
        context['end_date'] = self.request.GET.get('ed')
        context['venue'] = self.request.GET.get('v')
        context['city'] = self.request.GET.get('c')
        context['country'] = self.request.GET.get('co')
        # context['min_price'] = self.request.GET.get('mip')
        # context['max_price'] = self.request.GET.get('map')
        # context['purchased'] = self.request.GET.get('p')

        return context

