from django.shortcuts import render,redirect
from django.http import FileResponse, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

import os
import time
import pythoncom

from .models import ConversionCounter
from .forms import WordUploadForm

from .services.file_service import (
    generate_unique_name,
    get_converted_directory,
    delete_file,
)

from .services.guest_limit import (
    can_convert,
    increment_conversion,
)

from .converters.registry import (
    get_converter,
    get_target_formats,
)




def home(request):
    allowed, remaining = can_convert(request)

    if request.method == "POST":

        if not allowed:
            return render(
                request,
                "converter/home.html",
                {
                    "form": WordUploadForm(),
                    "remaining": remaining,
                    "guest_limit_reached": True,
                    "has_download": False,
                },
            )

        form = WordUploadForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            uploaded_file = form.cleaned_data[
                "document"
            ]

            source_format = (
                uploaded_file.name
                .split(".")[-1]
                .lower()
            )

            target_format = form.cleaned_data[
                "target_format"
            ]

            converter = get_converter(
                source_format,
                target_format,
            )

            if not converter:
                form.add_error(
                    None,
                    f"{source_format.upper()} → "
                    f"{target_format.upper()} "
                    f"is not supported."
                )

                return render(
                    request,
                    "converter/home.html",
                    {
                        "form": form,
                        "remaining": remaining,
                        "guest_limit_reached": False,
                        "has_download": False,
                    },
                )

            try:
                upload_dir = os.path.join(
                    settings.MEDIA_ROOT,
                    "uploads",
                )

                converted_dir = (
                    get_converted_directory()
                )

                os.makedirs(
                    upload_dir,
                    exist_ok=True,
                )

                os.makedirs(
                    converted_dir,
                    exist_ok=True,
                )

                unique_name = (
                    generate_unique_name(
                        uploaded_file.name
                    )
                )

                input_path = os.path.join(
                    upload_dir,
                    unique_name,
                )

                with open(
                    input_path,
                    "wb+",
                ) as destination:
                    for chunk in (
                        uploaded_file.chunks()
                    ):
                        destination.write(
                            chunk
                        )

                output_name = (
                    os.path.splitext(
                        unique_name
                    )[0]
                    + f".{target_format}"
                )

                output_path = os.path.join(
                    converted_dir,
                    output_name,
                )

                pythoncom.CoInitialize()

                converter.convert(
                    input_path,
                    output_path,
                )

                ConversionCounter.objects.create()

                if (
                    not request.user
                    .is_authenticated
                ):
                    increment_conversion(
                        request
                    )

                request.session[
                    "download_path"
                ] = output_path

                request.session[
                    "download_name"
                ] = output_name

                messages.success(
                    request,
                    "Your file has been converted successfully."
                )

                return redirect(
                    "home"
                )

            except Exception as e:
                form.add_error(
                    None,
                    f"Conversion failed: {e}"
                )

    else:
        form = WordUploadForm()

    context = {
        "form": form,
        "remaining": remaining,
        "guest_limit_reached": (
            not allowed
        ),
        "has_download": bool(
            request.session.get(
                "download_path"
            )
        ),
    }

    return render(
        request,
        "converter/home.html",
        context,
    )
    
    
    
def cleanup_files(*paths):
    print(
        "Cleanup thread started",
        flush=True,
    )

    time.sleep(10)

    for path in paths:
        delete_file(path)
        print(
            f"Deleted: {path}",
            flush=True,
        )
        
def get_formats(request):
    source = request.GET.get(
        "source",
        "",
    ).lower()

    formats = get_target_formats(
        source
    )

    return JsonResponse(
        {
            "formats": formats,
        }
    )        
    
    
@login_required
def admin_dashboard(request):

    if (
        not request.user.is_authenticated
        or not request.user.is_superuser
    ):
        return render(
            request,
            "403.html",
            status=403,
        )

    total_users = User.objects.count()
    total_conversions = (
        ConversionCounter.objects.count()
    )

    context = {
        "total_users": total_users,
        "total_conversions": total_conversions,
        "status": "Online",
        "version": "v1.0",
        "privacy_mode": "Enabled",
    }

    return render(
        request,
        "converter/admin_dashboard.html",
        context,
    )
    

def download_file(request):
    download_path = request.session.get(
        "download_path"
    )

    download_name = request.session.get(
        "download_name"
    )

    input_path = request.session.get(
        "input_path"
    )

    if not download_path:
        return redirect("home")

    response = FileResponse(
        open(download_path, "rb"),
        as_attachment=True,
        filename=download_name,
    )

    request.session.pop(
        "download_path",
        None,
    )

    request.session.pop(
        "download_name",
        None,
    )

    request.session.pop(
        "input_path",
        None,
    )

    original_close = response.close

    def cleanup():
        original_close()

        delete_file(download_path)
        delete_file(input_path)

    response.close = cleanup

    return response



