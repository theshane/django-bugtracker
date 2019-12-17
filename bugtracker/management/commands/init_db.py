import os
import sys
import bugtracker.models
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Adds default data to the database"

    def handle(self, *args, **options):
        self.add_statuses()

    def add_statuses(self):
        print("*** Adding statuses ***\n")
        for status in bugtracker.models.Status.get_status_enums():

            if bugtracker.models.Status.objects.filter(
                display_text=status["display_text"]
            ):
                print("{} already exists\n".format(status["display_text"]))
                continue

            print("Adding {}\n".format(status["display_text"]))
            new_status = bugtracker.models.Status(**status)
            new_status.save()
        print("*** Statuses added ***\n")
