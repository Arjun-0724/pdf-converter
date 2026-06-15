from django.shortcuts import render
from .forms import WordUploadForm

def home(request):

    if request.method == "POST":

        uploaded_file = request.FILES["document"]

        print(uploaded_file.name)

    form = WordUploadForm()

    return render(
        request,
        "converter/home.html",
        {
            "form": form
        }
    )