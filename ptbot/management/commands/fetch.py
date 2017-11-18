from django.conf import settings
from django.core.management import BaseCommand

from ptbot.fetcher import fetch_data


class Command(BaseCommand):
    help = "Management command to fetch fresh data"

    def handle(self, *args, **options):
        tokens = settings.PT_TOKENS
        for token in tokens:
            fetch_data(token=token)
