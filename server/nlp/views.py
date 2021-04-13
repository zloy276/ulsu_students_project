from django.core.files.storage import FileSystemStorage
from django.core.files import File
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
    data = NLP_1.main(doc.document)

    f = open(doc.document)
    f = File(f)
    document = models.Document.objects.create()

    document.upload_to = '{}/{}/documents/'.format(
        data['Факультет'], data['Направление'])
    document.document = f
    document.save()

    student = models.Student.objects.create(full_name=data['ФИО'], direction=data['Направление'], profile=[
                                            'Профиль'], topic=['Тема ВКР'], document=document)
    student.words_cloud = data['Частотный анализ слов']
    student.save()

    return render(request, 'show.html')
