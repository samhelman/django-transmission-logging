# DJANGO TRANSMISSION LOGGING

Django Transmission Logging is a simple Django app to standardise the
logging of request data.

## Quick Start

1. Add "transmission_logging" to your INSTALLED_APPS setting like this::

    ```python
    INSTALLED_APPS = [
        ...
        'transmission_logging',
    ]
    ```

2. Include the transmission_logging URLconf in your project urls.py like this:

    ```python
    path(
        'transmission-logging/', 
        include(
            ('transmission_logging.urls', 'transmission_logging'), namespace='transmission_logging'
        )
    ),
    ```

3. Run `python manage.py migrate` to create the transmission_logging models.

4. To log all incoming requests, add the transmission logging middleware in your MIDDLEWARE setting like this::

    ```python
    MIDDLEWARE = [
        ...
        'transmission_logging.middleware.TransmissionMiddleware',
    ]
    ```

5. To log exceptions in certain views, use the TransmissionLogMixin like this::

    ```python
    from transmission_logging.mixins import TransmissionLogMixin

    class MyView(TransmissionLogMixin, APIView):
        ...
    ```

## Advanced Settings

### TransmissionMiddleware Settings

1. TRANSMISSION_LOGGING_EXCLUDE_REQUEST_LOGGING (default: False). If this setting is set to True, the middleware will not log any incoming requests.

2. transmission_logging_exclude (default: False). If this view attribute is set to True, the middleware will not log incoming requests for that view:

    ```python
    from transmission_logging.mixins import TransmissionLogMixin

    class MyView(TransmissionLogMixin, APIView):
        transmission_logging_exclude = True
    ```

3. TRANSMISSION_LOGGING_INCLUDE_REQUEST_LOGGING_APPS (no default). If this setting is set, only apps that are defined in the list will have their requests logged. Should not be used in conjunction with TRANSMISSION_LOGGING_EXCLUDE_REQUEST_LOGGING_APPS.

    ```python
    TRANSMISSION_LOGGING_INCLUDE_REQUEST_LOGGING_APPS = [
        "admin",
        "api",
    ]
    ```

4. TRANSMISSION_LOGGING_EXCLUDE_REQUEST_LOGGING_APPS (default: ["admin"]). If this setting is set, requests will be logged for these apps. Requests will be logged for all other apps. Should not be used in conjunction with TRANSMISSION_LOGGING_INCLUDE_REQUEST_LOGGING_APPS.
    
    ```python
    TRANSMISSION_LOGGING_EXCLUDE_REQUEST_LOGGING_APPS = [
        "admin",
        "api",
    ]
    ```

### TransmissionLogMixin Settings

1. By default, the TransmissionLogMixin will return a django.http.JsonResponse with status code 500 in the case of an error. This can be overriden using the response_on_exception attribute:

    ```python
    class MyView(TransmissionLogMixin, APIView):
        response_on_exception = JsonResponse({"results": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    ```

## Actions

You can register additional actions in order to perform custom actions when the TransactionMiddleware is triggered. The custom_action function that you register must accept a single argument - the instance of the TransactionLog that is created by the middleware.

```python
from transmission_logging import middleware

def custom_action(instance):
    print("This is a custom action.")

middleware.actions.register(custom_action)
```

## Transmission Dashboard

### Model Registration

By default, the transmission dashboard will display the records for RequestLog and ResponseLog models.

You can register custom models with the transmission dashboard in a similar way to how the django admin works.

```python
from transmission_logging import transmission_dashboard

transmission_dashboard.register(CustomModel)
```

### Dashboard List View

By default, the dashboard list view will display a paginated list of all rows in the registered model table, with no filters.

There are some customisable options for the list view. 

You can change the list display values in a similar way to the django admin by adding list or tuple of strings to the registered model's list_display attribute.

You can also add a dropdown filter form to the list view by adding the list_filters attribute in a similar way to the list_display attribute. The fields in the list_filters do not necessarily have to be in the list_display.

```python
class RequestLog(TransmissionLog):
    ....
    list_filters = (
        "endpoint",
        "user",
    )
    list_display = (
        "endpoint",
        "user",
    )
```

### Dashboard Detail View

In order to display details on the transmission dashboard detail page, you should add a data property to the model that returns a dictionary of field names and values. For example, the RequestLog model:

```python
class RequestLog(TransmissionLog):
    ....
    @property
    def data(self):
        """
            Returns the serialized data for this instance.
        """
        # late import to handle circular import error
        from transmission_logging.serializers import RequestLogSerializer
        return RequestLogSerializer(self).data

class RequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestLog
        exclude = (
            "id",
        )

    user = serializers.CharField(source="user.username", allow_null=True, read_only=True)
```