from events.models import Category, Event
from django.views.generic import ListView
from django.db.models import Q
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
            results = results.filter(Q(category=category))
        
        # Filter by Broadcaster
        if broadcaster:
            results = results.filter(Q(broadcaster__icontains=broadcaster))

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


        # Filter by Time/Date

        # Filter by City/Country


        return results
    
    # If second search, keep original values
    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)

        # if you don't order_by brand first, distinct() doesn't seem to work.
        # context['brands'] = Event.objects.all().order_by('brand').values_list('brand', flat=True).distinct()

        context['is_search_page'] = True

        context['query'] = self.request.GET.get('q')
        context['sort_by'] = self.request.GET.get('s')
        context['q_category'] = self.request.GET.get('cat')
        context['q_broadcaster'] = self.request.GET.get('b')
        # context['min_price'] = self.request.GET.get('mip')
        # context['max_price'] = self.request.GET.get('map')
        # context['purchased'] = self.request.GET.get('p')

        if context['q_category']:
            context['category_name'] = Category.get_all_categories(Q(id=context['q_category']))[0].name
            # context['category_name'] = Event.objects.filter(Q(categories=context['q_category']))[0].name

        return context

