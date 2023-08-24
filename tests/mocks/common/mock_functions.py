from acai.common.records.requirements import requirements


@requirements(verbose=True)
def mock_func_verbose(event):
    return event
