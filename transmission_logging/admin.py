from django.contrib import admin

from transmission_logging.models import (
    RequestLog,
    ResponseLog,
)

admin.site.register(RequestLog)
admin.site.register(ResponseLog)