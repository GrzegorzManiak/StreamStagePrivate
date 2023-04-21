from rest_framework.decorators import api_view
from accounts.com_lib import authenticated, invalid_response, required_data, success_response, is_admin, paginate
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
    Report.objects.create(
        reason=data['reason'],
        r_user= target if data['type'] == 'user' else None,
        # r_event= target if data['type'] == 'event' else None,
        # r_review= target if data['type'] == 'review' else None,
        # r_broadcaster= target if data['type'] == 'broadcaster' else None,
        reporter=request.user,
    )

    # -- Return the report
    return success_response('Report submitted successfully')



@api_view(['GET'])
@is_admin()
@paginate(
    page_size=10,
    search_fields=['id', 'reason', 'reporter__username', 'r_user__username'], #'r_event__event_id', 'r_review__review_id', 'r_broadcaster__id'],
    order_fields=['id', 'reason', 'question', 'time', 'date', 'solved'],
    model=Report
)
def filter_reports(request, models, total_pages, page):
    # -- Return the response
    return success_response('reports', {
        'reports': [report.serialize() for report in models],
        'page': page,
        'per_page': 10,
        'total': len(models),
        'pages': total_pages,
    })



@api_view(['POST'])
@is_admin()
@required_data(['id'])
def update_report(request, data):
    # -- Get the report
    try: report = Report.objects.get(id=data['id'])
    except Report.DoesNotExist: return invalid_response('Report not found', status=404)

    # -- Update the report
    report.solved = True
    report.solved_by = request.user
    report.save()
    return success_response('Successfully updated report')
