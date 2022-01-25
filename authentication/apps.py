from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    # Once the user is registered the ready() method will get triggered which then imports the signals module
    def ready(self):
        import authentication.signals