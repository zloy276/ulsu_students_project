from datetime import timedelta
import pytz

from dateutil.utils import today
from django.core.management.base import BaseCommand

from contact.models.logs import ContactChangeHistoryLogging


class Command(BaseCommand):
    def handle(self, *args, **options):
        ВОт тут пиши функцию
        