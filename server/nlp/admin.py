
from django.contrib import admin
from . import models
from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from django.db.models import JSONField

@admin.register(models.Logs)
class SomeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

admin.site.register(models.Document)
admin.site.register(models.Student)
admin.site.register(models.Faculty)
admin.site.register(models.Direction)
admin.site.register(models.Department)
admin.site.register(models.UploadedFile)