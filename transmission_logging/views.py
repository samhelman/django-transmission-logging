from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldError
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from transmission_logging.models import (
    TransmissionLog,
    RequestLog,
    ResponseLog,
)
from transmission_logging.forms import (
    TransmissionListFilterForm,
)

import datetime

class TransmissionDashboardView(UserPassesTestMixin, ListView):
    context_object_name = "models"
    template_name = "transmission_logging/transmission_dashboard.html"
    transmission_logging_exclude = True

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        qs = TransmissionLog.registered_models

        for model_name, model in qs.items():
            sub_qs = model.objects.all()
            if hasattr(model, "transmission_dashboard_filters"):
                sub_qs = model.objects.filter(model.transmission_dashboard_filters)
            model.count = sub_qs.count()

        return qs

class TransmissionLogListView(UserPassesTestMixin, ListView):
    context_object_name = "transmissions"
    template_name = "transmission_logging/transmission_list.html"
    paginate_by = 25
    transmission_logging_exclude = True

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        LogModel = TransmissionLog.registered_models.get(self.kwargs.get("contenttype"))
        self.model = LogModel
        qs = LogModel.objects.all()

        for filter_name, filter_value in self.request.GET.items():
            if filter_value:
                try:
                    if filter_value == "None":
                        filter_value = None
                    qs = qs.filter(**{filter_name: filter_value})
                except FieldError:
                    pass

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        content_type = self.kwargs.get("contenttype")
        context["contenttype"] = content_type

        context["model"] = self.model

        context["form"] = TransmissionListFilterForm(
            initial=self.request.GET,
            model=self.model,
        )
        
        return context

class TransmissionLogDetailView(UserPassesTestMixin, DetailView):
    context_object_name = "transmission"
    template_name = "transmission_logging/transmission_detail.html"
    transmission_logging_exclude = True

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        LogModel = TransmissionLog.registered_models.get(self.kwargs.get("contenttype"))
        return LogModel.objects.all()
