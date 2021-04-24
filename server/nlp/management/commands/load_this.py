from datetime import timedelta
import pytz
from django.conf import settings
import os
import csv
from dateutil.utils import today
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = csv.reader(os.path.join(os.getcwd(), 'file.csv'))
        for row in reader:
            print(row)
