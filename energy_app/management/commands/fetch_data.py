# energy_app/management/commands/fetch_data.py

import time
from django.core.management.base import BaseCommand
from energy_app.views import fetch_and_store_data

class Command(BaseCommand):
    help = 'Continuously fetch sensor data from Firebase and store it in MySQL'

    def handle(self, *args, **options):
        self.stdout.write("Starting continuous data fetch...")
        try:
            while True:
                fetch_and_store_data()
                self.stdout.write(self.style.SUCCESS("Fetched and stored sensor data."))
                time.sleep(10)  # Pause for 10 seconds between fetches (adjust as needed)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Stopping continuous data fetch."))
