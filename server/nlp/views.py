from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .forms import DocumentForm
from django.urls import reverse
from . import models
from . import NLP_1


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            doc = models.UploadedFile.objects.all().order_by("-uploaded_at")[0]
            return redirect(reverse('show', kwargs={"pk": doc.id}))
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {
        'form': form
    })


def process_doc(request, pk):
    doc = models.UploadedFile.objects.get(pk=pk)
    print(doc.document)
    data=NLP_1.main(doc.document)
    print(data)
    return render(request, 'show.html')
