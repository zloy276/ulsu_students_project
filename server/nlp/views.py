from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .forms import DocumentForm

from .models import Student


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {
        'form': form
    })
