from rest_framework.decorators import api_view
from accounts.com_lib import authenticated, invalid_response, required_data, success_response
from events.models import EventReview

from accounts.models import Member, Broadcaster, Report
from events.models import Event, EventReview

@api_view(['POST'])
@authenticated()
@required_data(['type', 'r_id', 'reason'])
def submit_report(request, data):
    # -- Make sure the report isint over 4000 characters
    if len(data['reason']) > 4000: return invalid_response('Reason is too long')
    
    # -- Validate the target
    valid_targets = ['event', 'review', 'user', 'broadcaster']
    if data['type'] not in valid_targets: return invalid_response('Invalid target')

    # -- Try to get the target
    match data['type']:
        case 'event':
            try: target = Event.objects.get(event_id=data['r_id'])
            except Event.DoesNotExist: return invalid_response('Event does not exist')

        case 'review':
            try: target = EventReview.objects.get(review_id=data['r_id'])
            except EventReview.DoesNotExist: return invalid_response('Review does not exist')

        case 'user':
            try: target = Member.objects.get(username=data['r_id'].lower())
            except Member.DoesNotExist: return invalid_response('User does not exist')

        case 'broadcaster':
            try: target = Broadcaster.objects.get(id=data['r_id'])
            except Broadcaster.DoesNotExist: return invalid_response('Broadcaster does not exist')

    # -- Create the report
    report = Report.objects.create(
        reason=data['reason'],
        r_user= target if data['type'] == 'user' else None,
        r_event= target if data['type'] == 'event' else None,
        r_review= target if data['type'] == 'review' else None,
        r_broadcaster= target if data['type'] == 'broadcaster' else None,
        reporter=request.user,
    )

    # -- Return the report
    return success_response('Report submitted successfully')