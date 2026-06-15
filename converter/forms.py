from django import forms

class WordUploadForm(forms.Form):
    document = forms.FileField()