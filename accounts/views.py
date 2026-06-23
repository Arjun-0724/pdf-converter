from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .tokens import email_verification_token

from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from .tokens import email_verification_token
from .services import send_verification_email


def verify_email(request, uidb64, token):
    try:
        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )

        user = User.objects.get(pk=uid)


        token_valid = (
            email_verification_token.check_token(
                user,
                token
            )
        )


    except Exception as e:
    
        user = None
        token_valid = False

    if user and token_valid:
        user.is_active = True
        user.save()

        return render(
            request,
            "accounts/email_verified.html"
        )

    return render(
        request,
        "accounts/email_invalid.html"
    )

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(
            request.POST
        )

        if form.is_valid():

            user = form.save(
                commit=False
            )

            # User cannot login yet
            user.is_active = False
            user.save()
       

            token = email_verification_token.make_token(user)
       

            # Generate link
            uid = (
                urlsafe_base64_encode(
                    force_bytes(
                        user.pk
                    )
                )
            )

            token = (
                email_verification_token
                .make_token(
                    user
                )
            )

            verification_link = (
                request.build_absolute_uri(
                    reverse(
                        "verify_email",
                        args=[
                            uid,
                            token,
                        ],
                    )
                )
            )
            # Email body
            message = (
                render_to_string(
                    "accounts/verify_email.txt",
                    {
                        "user": user,
                        "verification_link":
                            verification_link,
                    },
                )
            )

            send_mail(
                subject=(
                    "Verify your email"
                ),
                message=message,
                from_email=None,
                recipient_list=[
                    user.email
                ],
            )

            messages.success(
                request,
                "Account created. "
                "Check your terminal "
                "for the verification link."
            )

            return redirect(
                "login"
            )

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        },
    )

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        # Check inactive user first
        try:
            user = User.objects.get(
                username=username
            )

            if (
                not user.is_active
                and
                user.check_password(
                    password
                )
            ):
                request.session["unverified_email"] = user.email
                messages.error(
                    request,
                    "Your email is not verified. "                
                )

                return redirect(
                    "login"
                )

        except User.DoesNotExist:
            pass

        # Normal login
        if form.is_valid():
            user = form.get_user()

            login(
                request,
                user,
            )

            messages.success(
                request,
                "Logged in successfully."
            )

            return redirect(
                "home"
            )

    else:
        form = AuthenticationForm()
        
        

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
            "show_resend": (
                "unverified_email" in request.session
    )
        },
    )

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home")


def resend_verification_public(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.filter(email=email).first()

            if user.is_active:
                messages.info(
                    request,
                    "Account already verified. Please login."
                )
                return redirect("login")

            send_verification_email(user, request)

            messages.success(
                request,
                "Verification email sent. Check your inbox."
            )

        except User.DoesNotExist:
            messages.error(
                request,
                "No account found with this email."
            )

        return redirect("login")

    return render(request, "accounts/resend_email.html")



def resend_verification_logged_in(request):
    user = request.user

    if user.is_authenticated and not user.is_active:
        send_verification_email(user, request)
        messages.success(
            request,
            "Verification email resent successfully."
        )

    return redirect("login")