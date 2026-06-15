from django.shortcuts import render
from .forms import WordUploadForm

def home(request):

    form = WordUploadForm()

    return render(
        request,
        "converter/home.html",
        {"form": form}
    )