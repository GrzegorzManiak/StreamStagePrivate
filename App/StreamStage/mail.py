from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_email(to: str, subject: str, body: str):
    print(body)
    
    try:
        message = Mail(
            from_email=settings.OUTBOUND_EMAIL,
            to_emails=to,
            subject=subject,
            html_content=body
        )

        sg = SendGridAPIClient(settings.SENDGIRD_TOKEN)
        sg.send(message)

    except Exception as e:
        print(e.message)
