from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings

from .forms import WordUploadForm

from docx2pdf import convert
import pythoncom
import os


def home(request):

    if request.method == "POST":
        form = WordUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            uploaded_file = form.cleaned_data["document"]

            upload_dir = os.path.join(
                settings.MEDIA_ROOT,
                "uploads"
            )

            os.makedirs(upload_dir, exist_ok=True)

            docx_path = os.path.join(
                upload_dir,
                uploaded_file.name
            )

            with open(docx_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            pdf_name = (
                os.path.splitext(uploaded_file.name)[0]
                + ".pdf"
            )

            pdf_path = os.path.join(
                upload_dir,
                pdf_name
            )

            pythoncom.CoInitialize()

            try:
                convert(docx_path, pdf_path)
            finally:
                pythoncom.CoUninitialize()

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