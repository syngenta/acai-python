from acai.firehose.requirements import requirements

call_list = []

class MockDataClass:
    def __init__(self, record):
        self.record = record
        self.initialized = True


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
    after=after_call,
    data_class=MockDataClass
)
def mock_firehose_full(event):
    full_results = []
    for mock_data_class in event.records:
        full_results.append(mock_data_class.initialized)
    return {'firehose_full': full_results}
