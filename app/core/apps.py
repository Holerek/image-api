from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    # def ready(self):
    #     # Import the management command here to avoid circular imports
    #     from .management.commands.create_default_plans import Command
    #     Command().handle()