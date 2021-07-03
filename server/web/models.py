from django.contrib.postgres.fields import JSONField
from django.db import models


class Tag(models.Model):
    name = models.CharField('Название', max_length=256)


class Teacher(models.Model):
    name = models.CharField('ФИО', max_length=128)


class Groups(models.Model):
    name = models.CharField('Название', max_length=128)


class Direction(models.Model):
    name = models.CharField('Название', max_length=256)
    groups = models.ManyToManyField(Groups)
    year_free_spots = JSONField(
        verbose_name='Данные о бесплатных местах',
        null=True,
        blank=True
    )


class Cathedra(models.Model):
    name = models.CharField('Название', max_length=256)
    teachers = models.ManyToManyField(Teacher)
    tags = models.ManyToManyField(Tag)
    directions = models.ManyToManyField(Direction)


class Faculty(models.Model):
    name = models.CharField('Название', max_length=256)
    vk_url = models.CharField('Ссылка на группу во Вконтакте', max_length=256)
    dekan = models.CharField('Имя Декана', max_length=128)
    faculties = models.ManyToManyField(Cathedra)
