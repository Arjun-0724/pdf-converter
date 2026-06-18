from django import forms
from django.conf import settings


OUTPUT_CHOICES = [
    ("pdf", "PDF"),
    ("png", "PNG"),
    ("jpg", "JPG"),
    ("docx", "DOCX"),
    ("rtf", "RTF"),
    ("xlsx", "XLSX"),
    ("csv", "CSV"),
    
]


class WordUploadForm(forms.Form):
    document = forms.FileField()

    target_format = forms.ChoiceField(
        choices=OUTPUT_CHOICES
    )

    def clean_document(self):
        file = self.cleaned_data["document"]

        if file.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                "File size cannot exceed 20 MB."
            )

        return file