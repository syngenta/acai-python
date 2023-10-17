import time

from acai_aws.generic.requirements import requirements

from tests.mocks.generic.mock_class import MockDataClass

call_list = []

def before_call(records, reqs):
    before_call.has_been_called = True
    global call_list
    call_list.append('before')


def after_call(records, result, reqs):
    after_call.has_been_called = True
    global call_list
    call_list.append('after')


@requirements(
    custom_requiremnent=True,
    before=before_call,
    after=after_call
)
def mock_generic(event):
    return {'generic': event.body}


@requirements(
    data_class=MockDataClass
)
def mock_generic_dc(data_class):
    return data_class


@requirements(timeout=1)
def mock_timeout(event):
    time.sleep(5)
    return event
