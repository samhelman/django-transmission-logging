# DJANGO TRANSMISSION LOGGING

Django Transmission Logging is a simple Django app to standardise the
logging of request data.

## Quick start

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
from transmission_logging import actions

def custom_action(instance):
    print("This is a custom action.")

actions.register(custom_post_save_action)
```