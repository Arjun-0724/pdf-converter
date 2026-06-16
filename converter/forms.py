from django import forms


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

    if file.size > 20 * 1024 * 1024:
        raise forms.ValidationError(
            "File size cannot exceed 20 MB."
        )

    return file