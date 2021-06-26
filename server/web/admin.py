from django.contrib import admin
from .models import Faculty, Cathedra, Direction, Teacher, Tag, Groups
from django_json_widget.widgets import JSONEditorWidget
from django.contrib.postgres import fields


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    pass


@admin.register(Cathedra)
class CathedraAdmin(admin.ModelAdmin):
    pass


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    pass
