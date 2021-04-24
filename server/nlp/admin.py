from django.contrib import admin
from . import models
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from .utils import ReadableJSONFormField
from .models import Some

@admin.register(models.Logs)
class SomeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'form_class': ReadableJSONFormField},
    }

admin.site.register(models.Document)
admin.site.register(models.Student)
admin.site.register(models.Faculty)
admin.site.register(models.Direction)
admin.site.register(models.Department)