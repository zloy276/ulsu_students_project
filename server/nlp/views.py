from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .forms import DocumentForm
from django.urls import reverse
from .models import Student,Document


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            doc=Document.objects.all().order_by("-uploaded_at")[0]
            return redirect(reverse('show',kwargs={"pk":doc.id}))
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {
        'form': form
    })

def process_doc(request,pk):
    doc=Document.objects.get(pk=pk)
    print(doc.document)
    return render(request,'show.html')