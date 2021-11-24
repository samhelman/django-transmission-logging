from rest_framework import status

from django.http import JsonResponse

import traceback

from transmission_logging import tools as logging_tools
from transmission_logging.models import (
    TransmissionLog,
)

class TransmissionLogMixin:
    response_on_exception = JsonResponse({"results": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_exception(self, exception):
        """
            Default implementation creates a TransmissionLog object - logging some details about the request.
        """
        self.transmission_log = TransmissionLog.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            endpoint=self.request.path,
            full_path=self.request.get_full_path(),
            request_header=logging_tools.get_headers(self.request),
            request_content=logging_tools.get_request_content(self.request),
            request_type=self.request.method,
            traceback=traceback.format_exc(),
            is_error=True,
        )
        return self.response_on_exception
    
    def dispatch(self, request, *args, **kwargs):
        """
            Stores the request object on the class to use in handle_exception method.
        """
        self.request = request
        return super().dispatch(request, *args, **kwargs)

            