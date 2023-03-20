# -- Imports
from rest_framework.decorators import api_view
from accounts.com_lib import authenticated, invalid_response, required_data, success_response
from events.models import EventReview

@api_view(['GET', 'POST'])
@authenticated()
@required_data(['page', 'sort', 'order'])
def get_reviews(request, data):
    """
        This view is used to get the reviews
        of the user
    """
    # -- Pagination
    try: page = int(data['page'])
    except ValueError: return invalid_response('Page must be an integer')

    valid_sorts = ['created', 'rating', 'likes']
    if data['sort'] not in valid_sorts: return invalid_response('Invalid sort')

    valid_orders = ['asc', 'desc']
    if data['order'] not in valid_orders: return invalid_response('Invalid order')

    per_page = 5
    sort = '-' + data['sort'] if data['order'] == 'desc' else data['sort']

    # -- Get the reviews
    reviews = EventReview.objects.filter(
        author=request.user
    ).order_by(sort)

    total_pages = int(len(reviews) / per_page)
    processed_reviews = []
    reviews = reviews[page * per_page: (page + 1) * per_page]
    for review in reviews:
        processed_reviews.append({
            'id': review.review_id,
            'event': review.event.event_id,
            'event_name': review.event.title,
            'rating': review.rating,
            'body': review.body,
            'title': review.title,
            'created': review.created,
            'likes': review.likes,
        })

    # -- Return the reviews
    return success_response('Reviews retrieved successfully', {
        'reviews': processed_reviews,
        'page': page,
        'per_page': per_page,
        'total': len(processed_reviews),
        'pages': total_pages,
    })
