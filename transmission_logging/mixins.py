from rest_framework import status

from django.http import JsonResponse

import json
import traceback

from transmission_logging import tools as logging_tools
from transmission_logging.models import (
    ResponseLog,
)

class ResponseLogMixin:
    response_on_exception = JsonResponse({"results": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_exception(self, exception):
        """
            Default implementation creates a ResponseLog object - logging some details about the request.
        """
        self.response_log = ResponseLog.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            endpoint=self.request.path,
            full_path=self.request.get_full_path(),
            status_code=self.response_on_exception.status_code,
            header=logging_tools.get_headers(self.request),
            content=json.loads(self.response_on_exception.content),
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