import os

from django_daemon_command.management.base import DaemonCommand
from django.conf import settings

from mysite.settings import BASE_DIR
from nlp.models import Faculty, Direction, Student, UploadedFile, Department
from nlp import algorithm
from nlp.signals import log_create


class Command(DaemonCommand):
    sleep = 5

    def handle(self, *args, **options):
        self.daemonize()

    def process(self, *args, **options):

        file = open(os.path.join(settings.BASE_DIR, 'vkr.txt')).readlines()
        d = file[0].replace('\n', '').split('\t')
        l = list()
        for i in file[1::]:
            t = {}
            f = i.replace('\n', '').split('\t')
            f = list(filter(lambda x: x, f))
            try:
                for j in range(len(d)):
                    t[d[j]] = f[j]
            except:
                continue
            l.append(t)
        for i in l:
            doc = UploadedFile.objects.filter(is_processed=False, document__icontains=i['FILE_NAME']).first()
            if doc:
                print('Файл найден')
                try:
                    data = algorithm.main(doc.document, mode='govno')
                except:
                    print('Скрипт пошел по пизде')
                    continue

                faculty = Faculty.objects.filter(name=i['FACULTY']).first()
                if not faculty:
                    faculty = Faculty.objects.create(name=i['FACULTY'])

                department = Department.objects.filter(name=i['CATHEDRA'], faculty=faculty).first()
                if not department:
                    department = Department.objects.create(name=i['CATHEDRA'], faculty=faculty)

                direction = Direction.objects.filter(name=i['PROFILE'], department=department).first()
                if not direction:
                    direction = Direction.objects.create(name=i['PROFILE'], department=department)

                student = Student.objects.create(full_name=i['STUDENT'], direction=direction, profile=i['GRP'],
                                                 topic=i['NAME'], document=doc.document)

                if data['Частотный анализ слов'] != 'Error':
                    student.words_cloud = data['Частотный анализ слов']
                    student.save()

                doc.is_processed = True
                doc.save()
                log_create(instance=student)
            else: print('Файл не найден', i['FILE_NAME'])