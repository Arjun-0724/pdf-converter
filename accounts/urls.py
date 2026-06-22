from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path(
        "verify-email/<uidb64>/<token>/",
        views.verify_email,
        name="verify_email"
    ),
    path("resend-verification/", views.resend_verification_public, name="resend_verification"),
    path("resend-verification-logged-in/", views.resend_verification_logged_in, name="resend_verification_logged_in"),
]