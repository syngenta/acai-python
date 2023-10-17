import time

from acai_aws.common.records.requirements import requirements


@requirements(verbose=True)
def mock_func_verbose(event):
    return event

@requirements(timeout=1)
def mock_func_timeout(event):
    time.sleep(5)
    return event
