from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .tokens import email_verification_token

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("home")

    else:
        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form}
    )

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # 🔒 IMPORTANT: user must not be active until verification
            user.is_active = False
            user.save()

            # UID + token
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            token = email_verification_token.make_token(user)

            domain = get_current_site(request).domain

            verification_link = (
                f"http://{domain}"
                f"{reverse('verify_email', args=[uid, token])}"
            )

            # Email content (console backend will print this)
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

            messages.success(
                request,
                "Account created! Please check your email to verify your account."
            )

            return redirect("login")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )