from accounts.com_lib import invalid_response, error_response, required_data, success_response
from rest_framework.decorators import api_view
from accounts.models import Member, Broadcaster

@api_view(['POST'])
@required_data(['broadcaster_id', 'name', 'biography'])
def edit_broadcaster_details(request, data):
    return success_response('Success', {})
