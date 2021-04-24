from django.db.models.signals import post_save
from .models import Student, Logs
from django.dispatch import receiver
import json


def model_create(*args, **kwargs):
    instance = kwargs.get("instance")
    info_arr = [instance.full_name, instance.words_cloud, instance.direction.name, instance.direction.department.name,
                instance.direction.department.faculty.name]
    if 'Error' in info_arr and instance.is_normal == True:
        instance.is_normal = False
        Logs.objects.create(student=instance, info=json.dumps(instance.__dict__, default=str))
        instance.save()


post_save.connect(log_create, sender=Student, weak=True)