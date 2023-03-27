from .models import *

from StreamStage import identifiers

from .models import STATUS_APPROVED, STATUS_REJECTED

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
        over_18 = False,
        biography = data['biography']
    )

    broadcaster.save()

    application = BroadcasterApplication(
        submission_statement = submission_statement,
        applicant = user,
        broadcaster = broadcaster
    )
    
    application.save()

def submit_event_application(user, data):
    event = Event(
        broadcaster = data['broadcaster'],
        title = data['title'],
        description = data['description'],
        over_18s = data['over_18s'],
        event_id = identifiers.generate_event_id(),
        #live_price = data['live_price']
    )
        # stream_price = data['stream_price'],

    #print(data['categories'])
    #for category in data['categories']:
    #    event.categories.add(category)

    event.save()

    application = EventApplication(
        applicant = user,
        event = event,
    )
    
    application.save()

    return event

# Reviewal / Admin Functionality
def approve_streamer_application(application, admin):
    application.status = STATUS_APPROVED
    application.processed_by = admin

    application.applicant.is_streamer = True
    application.applicant.save()
    application.save()

def reject_streamer_application(application, admin):
    application.status = STATUS_REJECTED
    application.processed_by = admin
    application.save()

def approve_broadcaster_application(application, admin):
    application.status = STATUS_APPROVED
    application.processed_by = admin

    application.broadcaster.approved = True
    application.save()

def reject_broadcaster_application(application, admin):
    application.status = STATUS_REJECTED
    application.processed_by = admin
    application.save()

def approve_event_application(application, admin):
    application.status = STATUS_APPROVED
    application.processed_by = admin

    application.event.approved = True
    application.event.save()
    application.save()

def reject_event_application(application, admin):
    application.status = STATUS_REJECTED
    application.processed_by = admin
    application.save()


# Utility Functions
def get_broadcaster_application(user):
    return BroadcasterApplication.objects.filter(applicant=user).first()

def get_streamer_application(user):
    return StreamerApplication.objects.filter(applicant=user).first()

def get_event_applications(user):
    return EventApplication.objects.filter(applicant=user).all()