from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_email(subject, body, to):
    message = Mail(
        from_email=settings.OUTBOUND_EMAIL,
        to_emails=to,
        subject=subject,
        html_content=body)
    try:
        sg = SendGridAPIClient(settings.SENDGIRD_TOKEN)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
