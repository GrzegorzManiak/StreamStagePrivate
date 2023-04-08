from accounts.com_lib import required_data, success_response, error_response, authenticated
from rest_framework.decorators import api_view
from .processing import (
    submit_broadcaster_application,
    submit_event_application,
    submit_streamer_application,

    get_broadcaster_applications,
    get_event_applications,
    get_streamer_applications,
)

from .models import ( STATUS_APPROVED, STATUS_REJECTED, STATUS_WAITING )


@api_view(['POST'])
@required_data(['submission_statement'])
def submit_streamer_app(request, data):

    submit_streamer_application(data)

    return success_response("Successfully submitted streamer application.")

@api_view(['POST'])
@required_data(['app_id'])
def submit_broadcaster_app(request, data):


    pass

@api_view(['POST'])
@required_data(['app_id'])
def submit_event_app(request, data):


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
