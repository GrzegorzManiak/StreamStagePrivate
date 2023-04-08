import secrets

from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from StreamStage.models import Statistics
from accounts.com_lib import invalid_response, required_data, success_response, is_admin
from StreamStage.models import Terms, Privacy

@api_view(['GET'])
@is_admin()
def site_panel(request):
    """
        This is the main site control panel
        allowing admins to manage the site
    """
    # -- Render the site panel
    return render(
        request,
        'admin/site_panel.html',
        context={
            'api': {
                'get_statistics': reverse_lazy('get_statistics'),

                'send_verification': reverse_lazy('send_verification'),
                'resend_verification': reverse_lazy('resend_key'),
                'remove_verification': reverse_lazy('remove_key'),
                'recent_verification': reverse_lazy('recent_key'),
                'users': reverse_lazy('users'),
                'get_user': reverse_lazy('get_user'),
                'update_email': reverse_lazy('update_user_email'),
                'delete_user': reverse_lazy('delete_user'),
                'update_streamer_status': reverse_lazy('update_streamer_status'),
            },
            'terms': Terms.latest(),
            'privacy': Privacy.latest(),
        }
    )



@api_view(['GET'])
@is_admin()
@required_data(['group', 'statistic', 'from', 'to', 'frame'])
def get_statistics(request, data):
    """
        This is the get method for the statistics view
        that is used to render the statistics page
    """
    # -- Make sure the frame is valid
    if data['frame'] not in ['seconds', 'minute', 'hour', 'day', 'week', 'month', 'year']:
        return invalid_response('Invalid frame')
        
    return success_response(
        "Statistics retrieved successfully",
        Statistics.build_statistic(
            data['group'], 
            data['statistic'],
            [ data['from'], data['to'] ],
            data['frame']
        )
    )