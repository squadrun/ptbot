from django.core.management import BaseCommand

from ptbot.fetcher import fetch_data


class Command(BaseCommand):
    help = "Management command to fetch fresh data"

    def handle(self, *args, **options):
        fetch_data()
