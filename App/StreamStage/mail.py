from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
from django.conf import settings
from django.apps import apps
import uuid

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
    # -- Should we log the email?
    log = True
    print(member)
    # -- Generate a new uuid
    email_id = str(uuid.uuid4())
    if template_id == 'verification': email = member
    else: email = member.email
    subject = ""
    body = ""

    base_context = {
        'email': email,
        'support_email': settings.SUPPORT_EMAIL,
        'year': '2023',
        'title': 'Title',
        'description': 'Description',
        'email_id': email_id,
        'user': member,
        'data': data
    }


    # -- Get the template
    match template_id:
        case 'welcome':
            log = False
            subject = "Welcome to StreamStage"
            base_context['title'] = "Welcome"
            base_context['description'] = "You have successfully registered an account"
            body = render_to_string(
                'email/welcome.html',
                base_context
            )
            
        case 'password_change':
            subject = "Password changed"
            base_context['title'] = "Password changed"
            base_context['description'] = "You have successfully changed your password"
            body = render_to_string(
                'email/password_change.html',
                base_context
            )

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

        case 'login_success':
            subject = "Successful login"
            base_context['title'] = "Login success"
            base_context['description'] = "You have successfully logged in"
            body = render_to_string(
                'email/login_success.html',
                base_context
            )

        case 'login_failed':
            subject = "Login failed"
            base_context['title'] = "Login failed"
            base_context['description'] = "You have failed to login"
            body = render_to_string(
                'email/login_failed.html',
                base_context
            )

        case 'verification':
            log = False
            subject = "Email verification"
            base_context['title'] = "Email verification"
            base_context['description'] = "Please verify access to your email address"
            body = render_to_string(
                'email/verification.html',
                base_context
            )
        
        case 'mfa_enabled':
            log = False
            subject = "MFA enabled"
            base_context['title'] = "MFA enabled"
            base_context['description'] = "You have successfully enabled MFA on your account"
            body = render_to_string(
                'email/mfa_enabled.html',
                base_context
            )

        case 'mfa_disabled':
            subject = "MFA disabled"
            base_context['title'] = "MFA disabled"
            base_context['description'] = "You have successfully disabled MFA on your account"
            body = render_to_string(
                'email/mfa_disabled.html',
                base_context
            )

        case 'mfa_recovery':
            subject = "MFA recovery"
            base_context['title'] = "MFA recovery"
            base_context['description'] = "You have used one of your recovery codes"
            body = render_to_string(
                'email/mfa_recovery.html',
                base_context
            )

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

    # -- Add the email to the database
    sent_email = apps.get_model('StreamStage', 'SentEmail')
    
    # -- Check if the 'member' has an id
    member_id = None
    if isinstance(member, dict):
        if 'id' in member:
            member_id = member['id']
        else: member_id = None

    if log: sent_email.objects.create(
        email=email,
        subject=subject,
        body=body,
        email_id=email_id,
        member_id=member_id
    )

    # -- Send out the email
    # send_email(email, subject, body)