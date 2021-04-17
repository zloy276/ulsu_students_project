from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.shortcuts import render, redirect
from .forms import DocumentForm
from django.urls import reverse
from .models import Faculty, Direction, Student, UploadedFile
from . import NLP_1


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            doc = UploadedFile.objects.all().order_by("-uploaded_at")[0]
            return redirect(reverse('show', kwargs={"pk": doc.id}))
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {
        'form': form
    })


def process_doc(request, pk):
    doc = UploadedFile.objects.get(pk=pk)
    data = NLP_1.main(doc.document)

    # f = open(doc.document)
    # f = File(f)
    # document = models.Document.objects.create()
    #
    # document.upload_to = '{}/{}/documents/'.format(
    #     data['Факультет'], data['Направление'])
    # document.document = f
    # document.save()
    print(data)

    faculty = Faculty.objects.filter(name=data['Факультет'])[0]
    if not faculty:
        faculty = Faculty.object.create(name=data['Факультет'])

    direction = Direction.objects.filter(name=data['Направление'], faculty=faculty)[0]
    if not direction:
        direction = Direction.object.create(name=data['Направление'], faculty=faculty)

    print(direction)

    student = Student.objects.create(full_name=data['ФИО'], direction=direction, profile=['Профиль'],
                                     topic=['Тема ВКР'], document=doc.document)

    if data['Частотный анализ слов'] != 'Error':
        student.words_cloud = data['Частотный анализ слов']
        student.save()

    return render(request, 'show.html')
