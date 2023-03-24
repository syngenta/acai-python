def mock_before_all(request, response, requirements):
    mock_before_all.has_been_called = True


def mock_after_all(request, response, requirements):
    mock_after_all.has_been_called = True


def mock_with_auth(request, response, requirements):
    mock_with_auth.has_been_called = True


def mock_on_error(request, response, error):
    mock_on_error.has_been_called = True
