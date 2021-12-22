from django.apps import AppConfig, apps
from django.conf import settings

from transmission_logging import transmission_dashboard

class TransmissionLoggingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transmission_logging'

    def ready(self):
        transmission_dashboard.register(apps.get_model("transmission_logging.RequestLog"))
        transmission_dashboard.register(apps.get_model("transmission_logging.ResponseLog"))