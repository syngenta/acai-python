def post(_, response):
    response.body = {'basic_mvvm_pattern': True}
    return response
