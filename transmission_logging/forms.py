from django import forms
from django.contrib.auth import get_user_model
from django.db import models

from transmission_logging.models import TransmissionLog

class TransmissionListFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model")
        super().__init__(*args, **kwargs)
        self._build_fields()
    
    def _build_fields(self):
        """
            For each field in the list of list_filters, add a choice field to the form.
        """
        for field_name in self.model.list_filters:
            self.fields[field_name] = forms.ChoiceField(
                choices=self._get_choices(field_name), 
                required=False,
            )

    def _get_choices(self, field_name):
        """
            Returns a list of distinct available choices from the model queryset field values.
        """
        values_list = self.model.objects.values_list(field_name, flat=True)
        field = self.model._meta.get_field(field_name)

        # If the field is a ForeignKey field, get the value of the fk instead of the pk.
        if isinstance(field, models.ForeignKey):
            choices = [(None, "")]
            for value in list(dict.fromkeys(values_list)):
                try:
                    choices.append((value, field.related_model.objects.get(id=value)))
                except field.related_model.DoesNotExist:
                    choices.append((str(value), str(value)))
        else:
            choices = [(None, "")] + [
                (str(value), str(value)) for value in list(dict.fromkeys(values_list))
            ]

        return list(dict.fromkeys(choices))