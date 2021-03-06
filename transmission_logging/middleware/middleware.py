from xml.dom.minidom import Attr
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

import traceback

from transmission_logging import tools as logging_tools
from transmission_logging.models import (
    RequestLog,
)

class TransmissionMiddleware(MiddlewareMixin):
    def _do_log(self, request, view_func, view_args, view_kwargs):
        """
            Returns a boolean that represents if the request should be logged or not.
        """
        # If TRANSMISSION_LOGGING_EXCLUDE_REQUEST_LOGGING setting is set to True, do not log transmissions.
        if getattr(settings, "TRANSMISSION_LOGGING_EXCLUDE_REQUEST_LOGGING", False):
            return False

        # If transmission_logging_exclude attribute is set to True on the view, do not log transmissions.
        try:
            if getattr(view_func.view_class, "transmission_logging_exclude", False):
                return False
        except AttributeError:
            pass
        
        # Only log transmissions the apps that have their app_name included in TRANSMISSION_LOGGING_INCLUDE_REQUEST_LOGGING_APPS setting, if that setting is defined.
        try:
            TRANSMISSION_LOGGING_INCLUDE_REQUEST_LOGGING_APPS = getattr(settings, "TRANSMISSION_LOGGING_INCLUDE_REQUEST_LOGGING_APPS")
            if resolve(request.path).app_name in TRANSMISSION_LOGGING_INCLUDE_REQUEST_LOGGING_APPS:
                return True
            return False
        except AttributeError:
            pass

        # If the app_name is included in TRANSMISSION_LOGGING_EXCLUDE_REQUEST_LOGGING_APPS setting, do not log transmissions. The setting defaults to ['admin'].
        if resolve(request.path).app_name in getattr(settings, "TRANSMISSION_LOGGING_EXCLUDE_REQUEST_LOGGING_APPS", ["admin"]):
            return False
        return True
    
    def _log_request(self, request):
        """
            Creates the RequestLog object. Returns an instance of RequestLog.
        """
        return RequestLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            endpoint=request.path,
            full_path=request.get_full_path(),
            header=logging_tools.get_headers(request),
            content=logging_tools.get_request_content(request),
            method=request.method,
        )

    def _perform_additional_actions(self, instance):
        """
            For each registered action, call the action function.
        """
        for action in RequestLog.actions:
            action(instance)

    def process_view(self, request, view_func, view_args, view_kwargs):
        """ 
            Logs details about requests before the view is processed.
        """
        if not self._do_log(request, view_func, view_args, view_kwargs):
            return

        instance = self._log_request(request)
        self._perform_additional_actions(instance)
