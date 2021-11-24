from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from transmission_logging.models import (
    TransmissionLog,
)
from transmission_logging.serializers import (
    TransmissionLogSerializer,
)
from transmission_logging.forms import (
    TransmissionListFilterForm,
)

class TransmissionLogListView(UserPassesTestMixin, ListView):
    model = TransmissionLog
    context_object_name = "transmissions"
    template_name = "transmission_logging/transmission_list.html"
    paginate_by = 25
    transmission_logging_exclude = True

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        qs = super().get_queryset()

        endpoint = self.request.GET.get("endpoint")
        user = self.request.GET.get("user")
        is_error = self.request.GET.get("is_error")

        # IF ENDPOINT IS A STRING AND NOT EMPTY, FILTER BY ENDPOINT
        if isinstance(endpoint, str) and endpoint:
            qs = qs.filter(endpoint=endpoint)

        if user:
            try:
                # IF THE USER ID HAS BEEN PASSED, FILTER BY USER_ID
                qs = qs.filter(user=int(user))
            except ValueError:
                # OTHERWISE, ASSUME "None" WAS PASSED
                qs = qs.filter(user=None)

        # FILTER BY is_error IF PASSED
        if is_error == "True":
            qs = qs.filter(is_error=True)

        if is_error == "False":
            qs = qs.filter(is_error=False)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = TransmissionListFilterForm(
            initial=self.request.GET,
        )
        
        return context

class TransmissionLogDetailView(UserPassesTestMixin, DetailView):
    model = TransmissionLog
    context_object_name = "transmission"
    template_name = "transmission_logging/transmission_detail.html"
    transmission_logging_exclude = True

    def test_func(self):
        return self.request.user.is_superuser
