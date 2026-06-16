from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings
from .models import *

from .forms import WordUploadForm

from docx2pdf import convert
import pythoncom
import os
from .services.file_service import *
import threading
import time

from .converters.registry import (
    get_converter
)

def home(request):
    recent_conversions = (
        Conversion.objects
        .order_by("-created_at")[:5]
    )

    if request.method == "POST":
        form = WordUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            uploaded_file = form.cleaned_data["document"]
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
                target_format
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
                        "recent_conversions":
                            recent_conversions,
                    }
                )
            unique_name = generate_unique_name(uploaded_file.name)

            upload_dir = os.path.join(
                settings.MEDIA_ROOT,
                "uploads"
            )

            os.makedirs(upload_dir, exist_ok=True)

            docx_path = os.path.join(
                upload_dir,
                unique_name
            )

            with open(docx_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            output_name = (
                os.path.splitext(unique_name)[0]
                + f".{target_format}"
            )
            
            converted_dir = get_converted_directory()
            

            output_path = os.path.join(
                converted_dir,
                output_name
            )

            pythoncom.CoInitialize()

            converter.convert(
                docx_path,
                output_path
            )
            
            Conversion.objects.create(
                original_name=uploaded_file.name,
                stored_name=output_name,
                source_format=source_format.upper(),
                target_format=target_format.upper(),
                status="Success"
            )
            threading.Thread(
                target=cleanup_files,
                args=(docx_path, output_path),
                daemon=True
            ).start()
            

            return FileResponse(
                open(output_path, "rb"),
                as_attachment=True,
                filename=output_name
            )

    else:
        form = WordUploadForm()

    return render(
        request,
        "converter/home.html",
        {
            "form": form,
            "recent_conversions": recent_conversions
        }
    )
    

def cleanup_files(*paths):
    print("Cleanup thread started", flush=True)

    time.sleep(10)

    for path in paths:
        delete_file(path)
        print(f"Deleted: {path}", flush=True)
    