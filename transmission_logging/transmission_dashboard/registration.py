
def register(model):
    # late import to avoid circular import error
    from transmission_logging.models import TransmissionLog
    TransmissionLog.registered_models[model._meta.model_name] = model
