from rest_framework.decorators import api_view
from ..models import Privacy
from accounts.com_lib import (
    is_admin,
    invalid_response,
    success_response,
    required_data,
    paginate
)


@api_view(['GET'])
@is_admin()
def get_latest_privacy(request):
    """
        Gets the latest privacy and conditions
    """
    # -- Get the privacy
    try: privacy = Privacy.latest()
    except Privacy.DoesNotExist:
        return invalid_response('No privacy and conditions found', status=404)
    return success_response('privacy and conditions', privacy.serialize())



@api_view(['POST'])
@is_admin()
@required_data(['content', 'title'])
def create_privacy(request, data):
    """
        Creates a new set of privacy and conditions
        and sets it as the latest (theres no way to
        update previous privacy and conditions)
    """
    # -- Create the privacy
    try: privacy = Privacy.create(title=data['title'], content=data['content'])
    except Exception as e: return invalid_response(str(e))
    return success_response('privacy and conditions', privacy.serialize())



@api_view(['GET'])
@is_admin()
@paginate(
    page_size=10,
    search_fields=['name', 'content'],
    order_fields=['name', 'content', 'created'],
    model=Privacy
)
def filter_privacy(request, models, total_pages, page):

    # -- Return the response
    return success_response('privacy and conditions', {
        'privacy': [privacy.serialize() for privacy in models],
        'page': page,
        'per_page': 10,
        'total': len(models),
        'pages': total_pages,
    })