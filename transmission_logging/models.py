from django.conf import settings
from django.db import models

import datetime

class TransmissionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    endpoint = models.TextField()
    full_path = models.TextField()
    header = models.JSONField()
    content = models.JSONField()
    method = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)

    # static models attribute used to register models for displaying in the dashboard
    registered_models = {}

    # static transmission_dashboard_filters attribute used to filter the count qs on the transmission logging dashboard
    transmission_dashboard_filters = models.Q(created_datetime__date=datetime.datetime.now().date())
    
    list_display = (
        "endpoint",
        "user",
        "created_datetime",
    )
    list_filters = (
        "endpoint",
        "user",
    )

    def __str__(self):
        return f"{self.endpoint} ({self.created_datetime})"

    class Meta:
        abstract = True
        ordering = ("-created_datetime",)

class RequestLog(TransmissionLog):
    # static actions attribute used to register functions for custom TransmissionMiddleware functionality
    actions = []

    transmission_dashboard_filters = TransmissionLog.transmission_dashboard_filters
    list_display = TransmissionLog.list_display
    list_filters = TransmissionLog.list_filters

    @property
    def data(self):
        """
            Returns the serialized data for this instance.
        """
        # late import to handle circular import error
        from transmission_logging.serializers import RequestLogSerializer
        return RequestLogSerializer(self).data  

class ResponseLog(TransmissionLog):
    status_code = models.IntegerField()
    traceback = models.TextField()
    is_error = models.BooleanField(default=False)

    transmission_dashboard_filters = TransmissionLog.transmission_dashboard_filters
    list_display = TransmissionLog.list_display
    list_filters = TransmissionLog.list_filters

    @property
    def data(self):
        """
            Returns the serialized data for this instance.
        """
        # late import to handle circular import error
        from transmission_logging.serializers import ResponseLogSerializer
        return ResponseLogSerializer(self).data