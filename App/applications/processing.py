from .models import *


def postEventApplication(form_data):

    
    pass

def approveStreamerApplication(application, admin):
    application.status = "APPROVED"
    application.processed_by = admin

    application.applicant.is_streamer = True

    if application.event:
        application.event.approved = True

def rejectStreamerApplication(application, admin):
    application.status = "REJECTED"
    application.processed_by = admin
