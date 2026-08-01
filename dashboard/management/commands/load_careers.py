from django.core.management.base import BaseCommand

from dashboard.models import CareerCatalog

from dashboard.career_data import CAREERS


class Command(BaseCommand):

    help = "Load careers into the database"

    def handle(self, *args, **kwargs):

        added = 0

        for career_name, icon, description in CAREERS:

            obj, created = CareerCatalog.objects.get_or_create(
                career_name=career_name,
                defaults={
                    "icon": icon,
                    "description": description,
                    "popular": True,
                },
            )

            if created:
                added += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added {added} careers."
            )
        )