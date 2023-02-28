from .models import *

# Submitting + Amending / User Functionality

def submit_streamer_application(user, data):
    submission_statement = data['submission_statement']

    application = StreamerApplication(
        submission_statement = submission_statement,
        applicant = user
    )
    
    application.save()

def submit_broadcaster_application(user, data):
    submission_statement = data['submission_statement']

    broadcaster = Broadcaster(
        streamer = user,
        handle = data['handle'],
        name = data['name'],
        over_18 = False
    )

    broadcaster.save()

    application = BroadcasterApplication(
        submission_statement = submission_statement,
        applicant = user,
        broadcaster = broadcaster
    )
    
    application.save()

def submit_event_application(user, data):
    submission_statement = data['submission_statement']

    broadcaster = Event(
        streamer = user,
        handle = data['handle'],
        name = data['name'],
        over_18 = False
    )

    broadcaster.save()

    application = BroadcasterApplication(
        submission_statement = submission_statement,
        applicant = user,
        broadcaster = broadcaster
    )
    
    application.save()

# Reviewal / Admin Functionality
def approveStreamerApplication(application, admin):
    application.status = "APPROVED"
    application.processed_by = admin

    application.applicant.is_streamer = True

    if application.event:
        application.event.approved = True

def rejectStreamerApplication(application, admin):
    application.status = "REJECTED"
    application.processed_by = admin

# Utility Functions

def get_broadcaster_application(user):
    return None

def get_streamer_application(user):
    return None