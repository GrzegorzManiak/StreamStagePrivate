from events.models import Category, Event, EventShowing, TicketListing
from django.views.generic import ListView
from django.db.models import Q
from datetime import datetime, timedelta
# from django.core.paginator import Paginator, EmptyPage, InvalidPage


class SearchResultsListView(ListView):
    model = Event
    context_object_name = 'events_list'
    template_name = 'search.html'
    # paginate_by = 10

    # Searching the events and returning results based on filters
    def get_queryset(self):
        user = self.request.user

        query = self.request.GET.get('q')
        category = self.request.GET.get('cat')
        broadcaster = self.request.GET.get('b')
        start_date = self.request.GET.get('sd')
        end_date = self.request.GET.get('ed')
        venue = self.request.GET.get('v')        
        city = self.request.GET.get('c')
        country = self.request.GET.get('co')
        upcoming = self.request.GET.get('u')
        todays_events = self.request.GET.get('t')
        in_person = self.request.GET.get('ip')
        sort = self.request.GET.get('s')
        min_price = self.request.GET.get('mip')
        max_price = self.request.GET.get('map')
        
        # Null Protection
        showings = None
        results = Event.objects.all()

        # Filter by Venue
        if venue:
            # Getting Venue from showings
            showings = (showings or EventShowing.objects).filter(venue=venue)

        # Filter by City
        if city:
            # Getting City from showings
            showings = (showings or EventShowing.objects).filter(city=city)

        # Filter by Country
        if country:
            # Getting Country from showings
            showings = (showings or EventShowing.objects).filter(country__name=country)

        # Filter by Date
        if end_date:
            end_date = datetime.strptime(end_date, '%d/%m/%Y').date()
            # Getting Showings before end date
            showings = (showings or EventShowing.objects).filter(time__lte=(end_date))

        if start_date:
            start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
            # Getting Showings after start date
            showings = (showings or EventShowing.objects).filter(time__gte=(start_date))
        
        # Show upcoming events only
        if upcoming == 'y':
            today = datetime.now().date()
            # Getting Showings after today
            showings = (showings or EventShowing.objects).filter(time__gte=today)

        # Show today's events only
        if todays_events == 'y':
            yesterday = datetime.now().date() - timedelta(days=1)
            tomorrow = datetime.now().date() + timedelta(days=1)
            # Getting Showings that are on today
            showings = (showings or EventShowing.objects).filter(time__gte=(yesterday)).filter(time__lte=(tomorrow))

        # If showings affect the filtering
        if showings is not None:
            # Matching Events to Showings
            events = []
            for showing in showings:
                events.append(showing.event)

            # Isolating event ID
            event_ids = []
            for event in events:
                event_ids.append(event.event_id)

            results = results.filter(event_id__in=event_ids).distinct()
        
        # Regular Search (User Input)
        if query:
            results = results.filter(Q(title__icontains=query) | Q(description__icontains=query) | 
                                     Q(broadcaster__handle__icontains=query) | Q(categories__name__icontains=query)).distinct()
        
        # Filter by Category
        if category:
            results = results.filter(Q(categories__name=category)).distinct()
        
        # Filter by Broadcaster
        if broadcaster:
            results = results.filter(Q(broadcaster__handle__icontains=broadcaster)).distinct()
        
        # Show in-person events only
        if in_person == 'y':
            # Getting Tickets between for events
            tickets = TicketListing.objects.filter().all()
            # Matching Events to Showings
            events = []
            for ticket in tickets:
                if ticket.ticket_type != 0:
                    events.append(ticket.event)

            # Isolating event ID
            event_ids = []
            for event in events:
                event_ids.append(event.event_id)

            results = results.filter(event_id__in=event_ids).distinct()

        # Filter by Price
        # Ascending
        if sort == 'price-asc':
            min_price_tickets = {}
            events = []
            for event in results:
                if event.has_ticket_listings() > 0:
                    # Get cheapest priced ticket for event
                    min_price_ticket = event.get_min_ticket_price()
                    # Add to list of cheapest priced tickets
                    min_price_tickets.update({min_price_ticket.price : min_price_ticket.event})
            # Order list by price
            sorted_prices = sorted(min_price_tickets.items(), key=lambda x:x[0])
            # Making list of events using ticket prices
            for ticket in sorted_prices:
                events.append(ticket[1])

            results = events
        # Descending
        elif sort == 'price-desc':
            min_price_tickets = {}
            events = []
            for event in results:
                if event.has_ticket_listings() > 0:
                    # Get cheapest priced ticket for event
                    min_price_ticket = event.get_min_ticket_price()
                    # Add to list of cheapest priced tickets
                    min_price_tickets.update({min_price_ticket.price : min_price_ticket.event})
            # Order list by price
            sorted_prices = sorted(min_price_tickets.items(), key=lambda x:x[0])
            # Making list of events using ticket prices
            for ticket in sorted_prices:
                events.append(ticket[1])

            results = events
            results.reverse()

        # Between two prices
        if min_price and max_price:
            min_price = int(min_price)
            max_price = int(max_price)

            if min_price == 0:
                max_price = 99999

            # Checking results between max and min price
            results = [ result for result in results if result.has_ticket_listings() and max_price >= result.get_min_ticket_price().price >= min_price 
            and max_price >= result.get_max_price_ticket().price >= min_price ]
        
        # Once filtering complete, return results
        return results
    
    # If second search, keep original values
    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)

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
        context['upcoming'] = self.request.GET.get('u')
        context['todays_events'] = self.request.GET.get('t')
        context['in_person'] = self.request.GET.get('ip')
        context['min_price'] = self.request.GET.get('mip')
        context['max_price'] = self.request.GET.get('map')

        return context
