from django.urls import path

from transmission_logging.views import (
    TransmissionLogListView,
    TransmissionLogDetailView,
)

urlpatterns = [
    path("", TransmissionLogListView.as_view(), name="transmission_list"),
    path("<int:pk>", TransmissionLogDetailView.as_view(), name="transmission_detail"),
]
