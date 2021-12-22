from rest_framework import serializers

from transmission_logging.models import (
    RequestLog,
    ResponseLog,
)

class RequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestLog
        exclude = (
            "id",
        )

    user = serializers.CharField(source="user.username", allow_null=True, read_only=True)

class ResponseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseLog
        exclude = (
            "id",
        )

    user = serializers.CharField(source="user.username", allow_null=True, read_only=True)