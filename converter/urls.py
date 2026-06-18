from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path( "formats/",
        views.get_formats,
        name="formats",
    ),
    path(
    "admin-portal-7x29/",
    views.admin_dashboard,
    name="admin_dashboard",
),
    path("download/",
        views.download_file,
        name="download_file",
    ),
]