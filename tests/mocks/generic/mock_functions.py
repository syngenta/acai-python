from acai.generic.requirements import requirements

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
def mock_generic_full(event):
    return {'generic_full': event.body}
