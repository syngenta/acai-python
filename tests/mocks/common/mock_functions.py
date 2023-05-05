from acai.common.records.requirements import requirements

@requirements()
def mock_func(event):
    result = {'event': []}
    for record in event.records:
        result['event'].append(record.body)
    return result


@requirements(verbose=True)
def mock_func_verbose(event):
    result = {'event': []}
    for record in event.records:
        result['event'].append(record.body)
    return result
