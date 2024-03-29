from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
from django.conf import settings
from django.apps import apps
from StreamStage.settings import RUNNING_ON_LOCALHOST, DEBUG, SEND_EMAILS
import uuid

def send_email(to: str, subject: str, body: str):    
    if RUNNING_ON_LOCALHOST: return
    if SEND_EMAILS == False: return
    if DEBUG: return
    
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
            base_context['title'] = "Payment method added"
            base_context['description'] = "You have successfully added a payment method"
            body = render_to_string(
                'email/payment_method_added.html',
                base_context
            )

        case 'payment_method_removed':
            subject = "Payment method removed"
            base_context['title'] = "Payment method removed"
            base_context['description'] = "You have successfully removed a payment method"
            body = render_to_string(
                'email/payment_method_removed.html',
                base_context
            )

        case 'email_change':
            subject = "Email changed"
            base_context['title'] = "Email changed"
            base_context['description'] = "You have successfully changed your email address"
            body = render_to_string(
                'email/email_change.html',
                base_context
            )


        case 'payment_success':
            subject = "Payment success"
            base_context['title'] = "Payment success"
            base_context['description'] = "You have successfully made a payment"
            body = render_to_string(
                'email/payment_success.html',
                base_context
            )


        case 'payment_canceled':
            subject = "Payment canceled"
            base_context['title'] = "Payment canceled"
            base_context['description'] = "You have canceled a payment"
            body = render_to_string(
                'email/payment_canceled.html',
                base_context
            )

        case 'subscription_success':
            subject = "Subscription success"
            base_context['title'] = "Subscription success"
            base_context['description'] = "You have successfully subscribed"
            body = render_to_string(
                'email/subscription_success.html',
                base_context
            )

        case 'change_password':
            subject = "Change password"
            base_context['title'] = "Change password"
            base_context['description'] = "You have requested to change your password"
            body = render_to_string(
                'email/change_password.html',
                base_context
            )
            


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
    if RUNNING_ON_LOCALHOST == False:
        send_email(email, subject, body)