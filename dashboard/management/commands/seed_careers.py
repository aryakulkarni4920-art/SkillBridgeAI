from django.core.management.base import BaseCommand
from dashboard.models import CareerCatalog
from dashboard.career_data import CAREERS


class Command(BaseCommand):
    help = "Insert default careers"

    def handle(self, *args, **kwargs):
        for name, icon, description in CAREERS:
            CareerCatalog.objects.get_or_create(
                career_name=name,
                defaults={
                    "icon": icon,
                    "description": description,
                    "popular": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Careers seeded successfully!"))