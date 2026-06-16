from django import forms

class WordUploadForm(forms.Form):

    document = forms.FileField(
        label="Select DOCX File"
    )

    def clean_document(self):

        document = self.cleaned_data["document"]

        if not document.name.endswith(".docx"):
            raise forms.ValidationError(
                "Only DOCX files are allowed."
            )

        return document