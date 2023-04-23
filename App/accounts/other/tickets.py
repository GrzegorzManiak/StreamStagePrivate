# -- Imports
from rest_framework.decorators import api_view
from accounts.com_lib import authenticated, invalid_response, required_data, success_response, impersonate
from accounts.models import Member

@api_view(['GET'])
@impersonate()
@authenticated()
def get_tickets(request):
    return success_response(
        'Tickets retrieved successfully',
        request.user.get_tickets()
    )