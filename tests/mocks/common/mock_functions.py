from acai.common.records.requirements import requirements


@requirements(verbose=True)
def mock_func_verbose(event):
    result = {'event': []}
    for record in event.records:
        result['event'].append(record.body)
    return result
