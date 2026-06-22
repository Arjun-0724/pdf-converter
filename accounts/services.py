from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .tokens import email_verification_token


def send_verification_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)

    domain = get_current_site(request).domain

    verification_link = (
        f"http://{domain}"
        f"{reverse('verify_email', args=[uid, token])}"
    )

    message = render_to_string(
        "accounts/verify_email.txt",
        {
            "user": user,
            "verification_link": verification_link,
        },
    )

    send_mail(
        subject="Verify your email - PDF Converter",
        message=message,
        from_email=None,
        recipient_list=[user.email],
    )