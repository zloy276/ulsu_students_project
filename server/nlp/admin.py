from django.contrib import admin
from . import models

admin.site.register(models.Document)
admin.site.register(models.Student)
admin.site.register(models.Faculty)
admin.site.register(models.Direction)
admin.site.register(models.Department)