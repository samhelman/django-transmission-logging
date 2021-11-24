from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import models

class TransmissionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    endpoint = models.TextField()
    full_path = models.TextField()
    request_header = models.JSONField()
    request_content = models.JSONField()
    request_type = models.TextField()
    traceback = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    is_error = models.BooleanField(default=False)

    # static actions attribute used to register functions for custom TransmissionMiddleware functionality
    actions = []

    def __str__(self):
        return f"{self.endpoint} ({self.created_datetime})"

    @property
    def data(self):
        """
            Returns the serialized data for this instance.
        """
        # late import to handle circular import error
        from transmission_logging.serializers import TransmissionLogSerializer
        return TransmissionLogSerializer(self).data

    class Meta:
        ordering = ("-created_datetime",)