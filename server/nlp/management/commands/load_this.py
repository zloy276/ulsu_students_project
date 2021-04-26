from datetime import timedelta
import pytz
import  pickle
from django.conf import settings
import os
import io
import csv
from django.core.files.base import ContentFile
from dateutil.utils import today
from django.core.management.base import BaseCommand
from nlp.models import UploadedFile


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.join(os.getcwd(), 'file.csv'), "r") as f_obj:
            reader = csv.reader(f_obj)
            mas = [row[0] for row in reader]
            files = os.listdir('{}/media/vkr'.format(settings.BASE_DIR))
            print(files)
            for file in files:
                if file in mas:
                    with open('{}/media/vkr/{}'.format(settings.BASE_DIR, file), "rb") as f:
                        UploadedFile.objects.create(document=ContentFile(f.read(),name=file))
