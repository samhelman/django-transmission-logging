from transmission_logging.models import (
    RequestLog,
)

def register(action):
    RequestLog.actions.append(action)