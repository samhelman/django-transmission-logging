from transmission_logging.models import (
    TransmissionLog,
)

def register(action):
    TransmissionLog.actions.append(action)