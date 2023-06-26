from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from the_shop import settings


def detect_user(user):
    if user.role is None and user.is_superadmin:
        return '/admin'
    role_dashboard = {
        'vendor': 'vendor-dashboard',
        'customer': 'customer-dashboard',
    }
    return role_dashboard.get(user.role)


def is_customer(user):
    """Returns True if the user us is customer"""
    if user.role == 'customer':
        return True
    raise PermissionDenied


def is_vendor(user):
    """Returns True if the user us is vendor"""
    if user.role == 'vendor':
        return True
    raise PermissionDenied


def send_email(request, mail_subject, email_template, user):
    """Send email"""
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    # -----------------------------------------------------------------------------------
    # mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    # mail.content_subtype = 'html'
    # mail.send()
    print(f'Subject: {mail_subject}\nFrom: {from_email}\nTo: {to_email}\n{message}')
    # -----------------------------------------------------------------------------------


def send_notification_email(mail_subject, mail_template, context):
    """Send notification email"""
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    if isinstance(context['to_email'], str):
        to_email = [context['to_email']]
    else:
        to_email = context['to_email']
    # -----------------------------------------------------------------------------------
    # mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    # mail.content_subtype = 'html'
    # mail.send()
    print(f'Subject: {mail_subject}\nFrom: {from_email}\nTo: {to_email}\n{message}')
    # -----------------------------------------------------------------------------------
