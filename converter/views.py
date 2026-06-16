from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings

from .forms import WordUploadForm

from docx2pdf import convert
import pythoncom
import os
from .services.file_service import *
import threading
import time

def home(request):

    if request.method == "POST":
        form = WordUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            uploaded_file = form.cleaned_data["document"]
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

            pdf_name = (
                os.path.splitext(unique_name)[0]
                    + ".pdf"
                )
            
            converted_dir = get_converted_directory()
            

            pdf_path = os.path.join(
                upload_dir,
                pdf_name
            )

            pythoncom.CoInitialize()

            convert(docx_path, pdf_path)
            
            threading.Thread(
                target=cleanup_files,
                args=(docx_path, pdf_path),
                daemon=True
            ).start()
            

            return FileResponse(
                open(pdf_path, "rb"),
                as_attachment=True,
                filename=pdf_name
            )

    else:
        form = WordUploadForm()

    return render(
        request,
        "converter/home.html",
        {
            "form": form
        }
    )
    

def cleanup_files(*paths):
    print("Cleanup thread started", flush=True)

    time.sleep(10)

    for path in paths:
        delete_file(path)
        print(f"Deleted: {path}", flush=True)
    