from django.urls import path

from transmission_logging.views import (
    TransmissionDashboardView,
    TransmissionLogListView,
    TransmissionLogDetailView,
)

urlpatterns = [
    path("", TransmissionDashboardView.as_view(), name="transmission_dashboard"),
    path("<str:contenttype>", TransmissionLogListView.as_view(), name="transmission_list"),
    path("<str:contenttype>/<int:pk>", TransmissionLogDetailView.as_view(), name="transmission_detail"),
]
