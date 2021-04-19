from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.
class Faculty(models.Model):
    name = models.CharField("Название", max_length=200, db_index=True)

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField("Название", max_length=200, db_index=True)
    faculty = models.ForeignKey(
        'Faculty', on_delete=models.CASCADE, verbose_name='Факультет')

    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'

    def __str__(self):
        return self.name


class Direction(models.Model):
    name = models.CharField("Название", max_length=200, db_index=True)
    faculty = models.ForeignKey(
        'Faculty', on_delete=models.CASCADE, verbose_name='Факультет', null=True)

    class Meta:
        verbose_name = 'Специльность'
        verbose_name_plural = 'Специльности'

    def __str__(self):
        return self.name


class Student(models.Model):
    full_name = models.CharField("ФИО", max_length=200, db_index=True)
    direction = models.ForeignKey(
        'Direction', on_delete=models.CASCADE, verbose_name="Направление", null=True)
    profile = models.CharField("Профиль", max_length=200)
    topic = models.CharField("Тема ВКР", max_length=200)
    departament = models.ForeignKey(
        'Department', on_delete=models.CASCADE, verbose_name="Кафедра", null=True)
    words_cloud = ArrayField(models.CharField(
        max_length=200), blank=True, verbose_name="Облако слов", null=True)
    document = models.FileField(upload_to='documents/', null=True)

    # report = models.ForeignKey(
    #     'ProcessedDocument', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('full_name',)
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return self.full_name


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document.name


class UploadedFile(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ProcessedDocument(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='processed_documents/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document.name
