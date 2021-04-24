from django.db.models.signals import post_save, post_delete, pre_save, pre_delete, m2m_changed
from .models import Student, Logs
from django.dispatch import receiver
import json


@receiver(post_save, sender=Student, weak=True)
def model_m2m_changed(*args, **kwargs):
    instance = kwargs.get("instance")
    info_arr = [instance.full_name, instance.words_cloud, instance.direction.name, instance.direction.department.name,
                instance.direction.department.faculty.name]
    if 'Error' in info_arr and instance.is_normal == True:
        instance.is_normal = False
        Logs.objects.create(student=instance, info=json.dumps(instance.__dict__, default=str))
        instance.save()