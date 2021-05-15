import os
from django.core.files.base import File
from django_daemon_command.management.base import DaemonCommand
from django.conf import settings
import shutil
from mysite.settings import BASE_DIR
from nlp.models import Faculty, Direction, Student, UploadedFile, Department
from nlp import algorithm
from nlp.signals import log_create


class Command(DaemonCommand):
    sleep = 5

    def handle(self, *args, **options):
        self.daemonize()

    def process(self, *args, **options):

        file = open(os.path.join(settings.BASE_DIR, 'VKR_1.txt')).readlines()
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
        file_list = os.listdir(path="/home/nlp/app/server/media/vkr")
        for i in l:
            file_name = i['FILE_NAME'].split('.')
            file_name = f'{file_name[0]}.{file_name[1].lower()}'
            print(file_name)
            if file_name in file_list:
                doc = open('/home/nlp/app/server/media/vkr/' + file_name)
                dj_file=File(doc)
                print('Файл найден')
                # shutil.copy(f'/home/nlp/app/server/media/vkr/{file_name}', f'/home/nlp/app/server/выборки/1_Выборка/{file_name}')
                try:
                    data = algorithm.main(doc, mode='govno')
                    if data=='doc':
                        print('ЭТО СРАНЫЙ DOC')
                        continue
                except:
                    print('Алгоритм обосрался')
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
                                                 topic=i['NAME'], document=dj_file)

                if data['Частотный анализ слов'] != 'Error':
                    student.words_cloud = data['Частотный анализ слов']
                    student.save()

                #doc.is_processed = True
                #doc.save()
                log_create(instance=student)
            else:
                print('Файл не найден', i['FILE_NAME'])


"""
000000000000000000000000000
000000001111000000000000000
000000010000100000000000000
000000100000010000000000000
000000100000010000000000000
000000100000010000000000000
000000100000010000000000000
000000100000010000000000000
001111100000011111000000000
010000100000010000100000000
010000000000000000100000000
001111111111111111000000000
000000000000000000000000000
000000000000000000000000000
000000000000000000000000000
"""
