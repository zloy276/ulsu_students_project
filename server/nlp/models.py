from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.

class Student(models.Model):
    full_name=models.CharField("ФИО", max_length=200,db_index=True)
    faculty=models.CharField("Факультет", max_length=200)
    directon=models.CharField("Направление", max_length=200)
    profile=models.CharField("Профиль", max_length=200)
    topic=models.CharField("Тема ВКР", max_length=200)
    word_cloud=ArrayField(models.CharField("Облако слов", max_length=200))

    class Meta:
        ordering=('full_name',)
        verbose_name='Студент'
        verbose_name_plural='Студенты'
    
    
    def __str__(self):
        return self.full_name


        