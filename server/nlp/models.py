from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.
class Faculty(models.Model):
    name = models.CharField("Название", max_length=200, db_index=True)


class Direction(models.Model):
    name = models.CharField("Название", max_length=200, db_index=True)
    faculty = models.ForeignKey(
        'Faculty', on_delete=models.CASCADE, verbose_name='Факультет')


class Student(models.Model):
    full_name = models.CharField("ФИО", max_length=200, db_index=True)
    faculty = models.ForeignKey(
        'Faculty', on_delete=models.CASCADE, verbose_name="Факультет")
    directon = models.ForeignKey(
        'Direction', on_delete=models.CASCADE, verbose_name='Направление')
    profile = models.CharField("Профиль", max_length=200)
    topic = models.CharField("Тема ВКР", max_length=200)
    words_cloud = ArrayField(models.CharField(
        max_length=200), blank=True, verbose_name="Облако слов")
    document = models.ForeignKey('Document', on_delete=models.CASCADE)
    processed_document = models.ForeignKey(
        'Processed_document', on_delete=models.CASCADE)

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


class Processed_document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='processed_documents/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document.name
