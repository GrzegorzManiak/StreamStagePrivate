from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
from django.conf import settings

def send_email(to: str, subject: str, body: str):    
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

    base_context = {
        'email': email,
        'support_email': settings.SUPPORT_EMAIL,
        'year': '2023',
        'title': 'Title',
        'description': 'Description',
        'email_id': '1234',
        'user': member,
        'data': data
    }


    # -- Get the template
    match template_id:
        case 'password_change':
            subject = "Password change"
            body = """
                <h1>Password change</h1>
            """

        case 'oauth_account_linked':
            subject = "Oauth account linked"
            base_context['title'] = "Account link"
            base_context['description'] = "You have successfully linked your account"
            body = render_to_string(
                'email/oauth_link.html',
                base_context
            )

        case 'oauth_account_removed':
            subject = "Oauth account removed"
            base_context['title'] = "Account unlink"
            base_context['description'] = "You have successfully unlinked your account"
            body = render_to_string(
                'email/oauth_unlink.html',
                base_context
            )

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

        case 'email_change':
            subject = "Email change"
            body = """
                <h1>Email change</h1>
            """
            

    send_email(email, subject, body)