from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_email(to: str, subject: str, body: str):
    print(body)
    
    try:
        email = Mail(
            from_email=settings.OUTBOUND_EMAIL,
            to_emails=to,
            subject=subject,
            html_content=body
        )

        sg = SendGridAPIClient(settings.SENDGIRD_TOKEN)
        sg.send(email)

    except Exception as e:
        print(e.message)


def send_template_email(
    member,
    template_id,
    data = None
): 
    email = member.email
    subject = ""
    body = ""

    # -- Get the template
    match template_id:
        case 'password_change':
            subject = "Password change"
            body = """
                <h1>Password change</h1>
            """

        case 'oauth_account_linked':
            subject = "Account link"
            body = """
                <h1>Account link</h1>
            """

        case 'oauth_account_removed':
            subject = "Account unlink"
            body = """
                <h1>Account unlink</h1>
            """

        case 'login':
            subject = "Login"
            body = """
                <h1>Login</h1>
            """

        case 'mfa_enabled':
            subject = "MFA enabled"
            body = """
                <h1>MFA enabled</h1>
            """

        case 'mfa_disabled':
            subject = "MFA disabled"
            body = """
                <h1>MFA disabled</h1>
            """

        case 'payment_method_added':
            subject = "Payment method added"
            body = """
                <h1>Payment method added</h1>
            """

        case 'payment_method_removed':
            subject = "Payment method removed"
            body = """
                <h1>Payment method removed</h1>
            """
            

    send_email(email, subject, body)