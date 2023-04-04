from rest_framework.decorators import api_view
from ..models import Terms
from accounts.com_lib import (
    is_admin,
    invalid_response,
    success_response,
    required_data,
    paginate
)


@api_view(['GET'])
@is_admin()
def get_latest_terms(request):
    """
        Gets the latest terms and conditions
    """
    # -- Get the terms
    try: terms = Terms.latest()
    except Terms.DoesNotExist:
        return invalid_response('No terms and conditions found', status=404)
    return success_response('Terms and conditions', terms.serialize())



@api_view(['POST'])
@is_admin()
@required_data(['content', 'title'])
def create_terms(request, data):
    """
        Creates a new set of terms and conditions
        and sets it as the latest (theres no way to
        update previous terms and conditions)
    """
    # -- Create the terms
    try: terms = Terms.create(title=data['title'], content=data['content'])
    except Exception as e: return invalid_response(str(e))
    return success_response('Terms and conditions', terms.serialize())



@api_view(['GET'])
@is_admin()
@paginate(
    page_size=10,
    search_fields=['name', 'content'],
    order_fields=['name', 'content', 'created', 'updated'],
    model=Terms
)
def filter_terms(request, models, total_pages, page):

    # -- Return the response
    return success_response('Terms and conditions', {
        'terms': [terms.serialize() for terms in models],
        'page': page,
        'per_page': 10,
        'total': len(models),
        'pages': total_pages,
    })