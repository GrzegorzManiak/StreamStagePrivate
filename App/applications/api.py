from accounts.com_lib import required_data, success_response, error_response, authenticated, is_admin
from rest_framework.decorators import api_view
from .processing import (
    submit_broadcaster_application,
    submit_event_application,
    submit_streamer_application,

    approve_streamer_application,
    approve_broadcaster_application,
    approve_event_application,
    reject_broadcaster_application,
    reject_event_application,
    reject_streamer_application,

    get_broadcaster_applications,
    get_event_applications,
    get_streamer_applications,
)

from .models import (
    EventApplication,
    StreamerApplication,
    BroadcasterApplication,

    STATUS_APPROVED,
    STATUS_REJECTED,
    STATUS_WAITING
)


# USER APIs

@api_view(['POST'])
@required_data(['submission_statement'])
@authenticated()
def submit_streamer_app(request, data):

    # Check if user has alreadyy submitted an event application
    if get_streamer_applications(request.user).count() > 0:
        return error_response("You can not submit an event application with another pending.")
    
    submit_streamer_application(request.user, data)

    return success_response("Successfully submitted streamer application.")

@api_view(['POST'])
@required_data(['handle', 'name', 'biography'])
@authenticated()
def submit_broadcaster_app(request, data):

    # ensure user is either a streamer or has an application pending
    if not request.user.is_streamer and get_streamer_applications(request.user).count() == 0:
        return error_response("You can not submit a broadcaster application application without submitting a streamer application first.")

    submit_broadcaster_application(request.user, data)

    pass

@api_view(['POST'])
@required_data(['broadcaster', 'title', 'description', 'categories', 'over_18s'])
def submit_event_app(request, data):

    # ensure user is either a streamer or has an application pending
    if not request.user.is_streamer and get_streamer_applications(request.user).count() == 0:
        return error_response("You can not submit an event application before submitting a streamer application.")

    # ensure user has a broadcaster application pending, or is already
    # authorized to act on behalf of a broadcaster
    if get_broadcaster_applications(request.user, [ STATUS_WAITING, STATUS_APPROVED ]).count() == 0:
        return error_response("You can not submit an event application without a pending or accepted broadcaster application.")

    submit_event_application(request.user, data)

    pass

@api_view(['POST'])
@authenticated()
def get_user_applications(request):
    applications = {
        "event": [],
        "broadcaster": [],
        "streamer": []
    }

    # serialize event applications
    for event_app in get_event_applications(request.user, [ STATUS_WAITING, STATUS_APPROVED, STATUS_REJECTED ]):
        serialized = {
            "application_id": event_app.application_id,
            "event_id": event_app.event.event_id,
            "submitted": event_app.submitted,
            "status": stream_app.status
        }

        if event_app.processed_by:
            serialized["processed_by"] = event_app.processed_by.cased_username

        applications["event"].append(serialized)
    
    # serialize streamer applications
    for stream_app in get_streamer_applications(request.user, [ STATUS_WAITING, STATUS_APPROVED, STATUS_REJECTED ]):
        serialized = {
            "application_id": stream_app.application_id,
            "submission_statement": stream_app.submission_statement,
            "submitted": stream_app.submitted,
            "status": stream_app.status
        }

        applications["streamer"].append(serialized)

    # serialize broadcaster applications
    for broad_app in get_broadcaster_applications(request.user, [ STATUS_WAITING, STATUS_APPROVED, STATUS_REJECTED ]):
        serialized = {
            "application_id": broad_app.application_id,
            "submission_statement": broad_app.submission_statement,
            "broadcaster_handle": "@" + broad_app.broadcaster.handle,
            "submitted": broad_app.submitted,
            "status": broad_app.status
        }

        applications["broadcaster"].append(serialized)

    return success_response("Successfully retrieved applications. ", { "applications": applications })


# Admin APIs

@api_view(['POST'])
@is_admin()
def fetch_pending_applications(request):
    streamers = []
    broadcasters = []
    events = []

    for application in get_streamer_applications(None):
        streamers.append({
            "application_id": application.application_id,
            "applicant": application.applicant.cased_username,
            "statement": application.submission_statement
        })

    for application in get_broadcaster_applications(None):
        broadcasters.append({
            "application_id": application.application_id,
            "applicant": application.applicant.cased_username,
            "handle": application.broadcaster.handle,
            "statement": application.submission_statement
        })

    for event in get_event_applications(None):
        events.append({
            "application_id": application.application_id,
            "applicant": application.applicant.cased_username,
            "handle": application.broadcaster.handle,
            "event_id": application.event.event_id,
            "event_title": application.event.title,
            "statement": application.submission_statement
        })

    return success_response("Successfully fetched applications.", { "streamers": streamers, "broadcasters": broadcasters, "events": events })


@api_view(['POST'])
@required_data(['type', 'application_id', 'status'])
@is_admin()
def update_application_status(request, data):
    type = data['type']
    status = data['status']

    if not status in [ STATUS_APPROVED, STATUS_REJECTED ]:
        return error_response("Invalid status given.")
    

    if type == 'streamer':
        try:
            app = StreamerApplication.objects.get(application_id=data['application_id'])

            if status == STATUS_APPROVED:
                approve_streamer_application(app, request.user)
            else:
                reject_streamer_application(app, request.user)
        except StreamerApplication.DoesNotExist:
            return error_response('Invalid application ID provided.')
    elif type == 'broadcaster':
        try:
            app = BroadcasterApplication.objects.get(application_id=data['application_id'])

            if status == STATUS_APPROVED:
                approve_broadcaster_application(app, request.user)
            else:
                reject_broadcaster_application(app, request.user)
        except BroadcasterApplication.DoesNotExist:
            return error_response('Invalid application ID provided.')
    elif type == 'event':
        try:
            app = EventApplication.objects.get(application_id=data['application_id'])

            if status == STATUS_APPROVED:
                approve_event_application(app, request.user)
            else:
                reject_event_application(app, request.user)
        except EventApplication.DoesNotExist:
            return error_response('Invalid application ID provided.')

    return error_response("An unknown error has occured. Please try again later.") 
        