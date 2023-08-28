from acai_aws.dynamodb.event_client import EventClient


def handler_requirements():
    def decorator_func(func):
        def wrapper(event, context):
            client = EventClient(event, context)
            return func(client)
        return wrapper
    return decorator_func
