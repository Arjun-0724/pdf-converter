from django import forms
from .services.file_service import *

class WordUploadForm(forms.Form):
    document = forms.FileField()

    def clean_document(self):
        file = self.cleaned_data["document"]

        allowed_extensions = [
            ".docx"
        ]

        extension = (
            "." +
            file.name.split(".")[-1].lower()
        )

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Only DOCX files are allowed."
            )

        if file.size > 20 * 1024 * 1024:
            raise forms.ValidationError(
                "File size cannot exceed 20 MB."
            )

        return file