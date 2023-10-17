import time

from acai_aws.apigateway.requirements import requirements

call_order = []

class TestDataClass:
    def __init__(self, request):
        self.request = request
        self.initialized = True


def before_call(request, response, reqs):
    before_call.has_been_called = True
    global call_order
    call_order.append('before')
    pass


def after_call(request, response, reqs):
    after_call.has_been_called = True
    global call_order
    call_order.append('after')
    pass


@requirements(
    custom_requiremnent=True,
    before=before_call,
    after=after_call,
    data_class=TestDataClass
)
def post(data_class, response):
    response.body = {'requirements_basic': data_class.initialized}
    return response


@requirements()
def get(_, response):
    time.sleep(5)
    response.body = {'timeout_basic': 'timeout'}
    return response

@requirements(timeout=1)
def patch(_, response):
    time.sleep(5)
    response.body = {'timeout_basic': 'timeout'}
    return response
