from django import forms
from django.contrib.auth import get_user_model

from transmission_logging.models import TransmissionLog

class TransmissionListFilterForm(forms.Form):
    endpoint = forms.ChoiceField(choices=(), required=False)
    user = forms.ChoiceField(choices=(), required=False)
    is_error = forms.ChoiceField(choices=(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_choices()
    
    def _build_choices(self):
        for field_name, field in self.fields.items():
            try:
                choices_func = getattr(self, f"get_{field_name}_choices")
                choices = choices_func()
            except AttributeError:
                choices = []
            field.choices = choices

    def get_endpoint_choices(self):
        return [(None, "")] + [
            (value, value)
            for value in list(dict.fromkeys(TransmissionLog.objects.values_list("endpoint", flat=True)))
        ]

    def get_user_choices(self):
        return [(None, ""), ("None", "None")] + [
            (value.pk, value.username)
            for value in get_user_model().objects.filter(transmissionlog__isnull=False).distinct()
        ]

    def get_is_error_choices(self):
        return [
            (None, ""),
            (True, True),
            (False, False),
        ]