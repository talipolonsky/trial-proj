from django.apps import AppConfig


class Plus500Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plus500'

    def ready(self):
        from updateservice import scheduler
        scheduler.start()
