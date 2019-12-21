import os
import sys
import bugtracker.models
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Adds default data to the database"

    def add_arguments(self, parser):
        parser.add_argument("--quiet", type=bool, default=False)

    def handle(self, *args, **options):
        self.quiet = options["quiet"]
        self.add_statuses()
        self.add_ticket_types()

    def add_statuses(self):
        self.display("*** Adding statuses ***\n")
        for status in bugtracker.models.Status.get_status_enums():

            if bugtracker.models.Status.objects.filter(
                display_text=status["display_text"]
            ):
                self.display("{} already exists\n".format(status["display_text"]))
                continue

            self.display("Adding {}\n".format(status["display_text"]))
            new_status = bugtracker.models.Status(**status)
            new_status.save()
        self.display("*** Statuses added ***\n")

    def add_ticket_types(self):
        self.display("*** Adding ticket types ***\n")
        for ticket_type in bugtracker.models.TicketType.get_ticket_type_enums():

            if bugtracker.models.Status.objects.filter(display_text=ticket_type):
                self.display("{} already exists\n".format(ticket_type))
                continue

            self.display("Adding {}\n".format(ticket_type))
            new_status = bugtracker.models.Status(display_text=ticket_type)
            new_status.save()
        self.display("*** Ticket types added ***\n")

    def display(self, text):
        if not self.quiet:
            print(text)
