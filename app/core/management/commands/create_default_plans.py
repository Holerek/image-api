"""
Django command for creating default plans in database.
"""
from django.core.management.base import BaseCommand

from core.models import Plan, Thumbnail, list_of_default_plans


class Command(BaseCommand):
    """Django command for creating default plans"""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        default_plans = list_of_default_plans()
        for plan in default_plans:
            thumbnails = plan.pop('thumbnails')
            p, created = Plan.objects.get_or_create(name=plan['name'], defaults=plan)

            for thumbnail in thumbnails:
                t, _ = Thumbnail.objects.get_or_create(size=thumbnail['size'])
                p.thumbnails.add(t)

            p.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created default plan: {p.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Plan already exists: {p.name}'))
