from django_daemon_command.management.base import DaemonCommand
from nlp.models import Faculty, Direction, Student, UploadedFile, Department
from nlp import algorithm
from nlp.signals import log_create


class Command(DaemonCommand):
    sleep = 5

    def handle(self, *args, **options):
        self.daemonize()

    def process(self, *args, **options):
        for doc in UploadedFile.objects.filter(is_processed=False):
            try:
                data = algorithm.main(doc.document)
            except:
                continue

            if len(data['Факультет']) > 150 or len(data['Кафедра']) > 150 or len(data['Направление']) > 150 or len(
                    data['ФИО']) > 150 or len(data['Тема ВКР']) > 150 or len(data['Профиль']) > 150:
                continue

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
