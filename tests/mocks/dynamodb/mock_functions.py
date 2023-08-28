from acai_aws.dynamodb.requirements import requirements

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
    data_class=MockDataClass,
    operations=['created', 'deleted']
)
def mock_ddb_full(event):
    full_results = []
    for mock_data_class in event.records:
        full_results.append(mock_data_class.initialized)
    return {'ddb_full': full_results}


@requirements()
def mock_ddb_basic(event):
    basic_results = []
    for record in event.records:
        basic_results.append(record.name)
    return {'ddb_basic': basic_results}

@requirements(
    operations=['deleted']
)
def mock_ddb_operation_ignore(event):
    ignored_results = []
    for record in event.records:
        ignored_results.append(record.name)
    return {'ddb_operation_ignore': ignored_results}


@requirements(
    operations=['deleted'],
    raise_operation_error=True
)
def mock_ddb_operation_raise(event):
    ignored_results = []
    for record in event.records:
        ignored_results.append(record.name)
    return {'ddb_operation_ignore': ignored_results}
