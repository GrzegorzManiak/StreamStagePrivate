# -- Imports
from rest_framework.decorators import api_view
from accounts.com_lib import authenticated, invalid_response, required_data, success_response, impersonate
from events.models import EventReview
from accounts.models import Member

@api_view(['GET', 'POST'])
@required_data(['page', 'sort', 'order', 'username'])
def get_reviews(request, data):
    """
        This view is used to get the reviews
        of the user
    """
    
    # -- Pagination
    try: 
        page = int(data['page'])
        if page < 0: return invalid_response('Page must be greater than 0')
    except ValueError: return invalid_response('Page must be an integer')

    valid_sorts = ['created', 'rating', 'likes']
    if data['sort'] not in valid_sorts: return invalid_response('Invalid sort')

    valid_orders = ['asc', 'desc']
    if data['order'] not in valid_orders: return invalid_response('Invalid order')

    per_page = 5
    sort = '-' + data['sort'] if data['order'] == 'desc' else data['sort']

    # -- Get the user
    try: user = Member.objects.get(username=data['username'].lower())
    except Member.DoesNotExist: return invalid_response('User does not exist')

    # -- Get the reviews
    reviews = EventReview.objects.filter(
        author=user
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
            'username': review.author.username,
        })

    # -- Return the reviews
    return success_response('Reviews retrieved successfully', {
        'reviews': processed_reviews,
        'page': page,
        'per_page': per_page,
        'total': len(processed_reviews),
        'pages': total_pages,
    })



@api_view(['POST'])
@impersonate()
@authenticated()
@required_data(['id', 'rating', 'title', 'body'])
def update_review(request, data):
    """
        This view is used to update the review
    """
    # -- Get the review
    review = EventReview.objects.filter(
        author=request.user,
        review_id=data['id']
    ).first()

    if review is None:
        return invalid_response('Review not found')

    # -- Check if the rating is valid
    if data['rating'] < 1 or data['rating'] > 10:
        return invalid_response('Invalid rating')

    title = data['title'].replace('<', '&lt;').replace('>', '&gt;')
    if len(title) < 1 or len(title) > 50:
        return invalid_response('Invalid title')
    
    body = data['body'].replace('<', '&lt;').replace('>', '&gt;')
    if len(body) < 1 or len(body) > 3096:
        return invalid_response('Invalid body')
    
    # -- Update the review
    review.rating = int(data['rating'])
    review.title = data['title']
    review.body = data['body']
    review.save()

    # -- Return the review
    return success_response('Review updated successfully')



@api_view(['POST'])
@impersonate()
@authenticated()
@required_data(['id'])
def delete_review(request, data):
    """
        This view is used to delete the review
    """

    # -- Get the review
    review = EventReview.objects.filter(
        author=request.user,
        review_id=data['id']
    ).first()

    if review is None:
        return invalid_response('Review not found')
    
    # -- Delete the review
    review.delete()

    # -- Return the review
    return success_response('Review deleted successfully')
