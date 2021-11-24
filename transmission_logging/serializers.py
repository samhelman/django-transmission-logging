from rest_framework import serializers

from transmission_logging.models import (
    TransmissionLog,
)

class TransmissionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmissionLog
        exclude = (
            "id",
        )

    user = serializers.CharField(source="user.username", allow_null=True, read_only=True)