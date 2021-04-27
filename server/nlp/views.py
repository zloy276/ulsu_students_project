from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.shortcuts import render, redirect
from .forms import DocumentForm
from django.urls import reverse
from .models import Faculty, Direction, Student, UploadedFile, Department
from . import algorithm
from .signals import log_create


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
    data = algorithm.main(doc.document)

    faculty = Faculty.objects.filter(name=data['Факультет']).first()
    if not faculty:
        faculty = Faculty.objects.create(name=data['Факультет'])

    department = Department.objects.filter(name=data['Кафедра'], faculty=faculty).first()
    if not department:
        department = Department.objects.create(name=data['Кафедра'], faculty=faculty)

    direction = Direction.objects.filter(name=data['Направление'], department=department).first()
    if not direction:
        direction = Direction.objects.create(name=data['Направление'], department=department)

    student = Student.objects.create(full_name=data['ФИО'], direction=direction, profile=data['Профиль'],
                                     topic=data['Тема ВКР'], document=doc.document)

    if data['Частотный анализ слов'] != 'Error':
        student.words_cloud = data['Частотный анализ слов']
        student.save()

    doc.is_processed = True
    doc.save()
    log_create(instance=student)

    return render(request, 'show.html', {"student": student})
