from django.contrib import admin

from transmission_logging.models import (
    TransmissionLog,
)

admin.site.register(TransmissionLog)