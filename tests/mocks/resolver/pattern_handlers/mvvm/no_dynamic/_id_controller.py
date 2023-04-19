def post(_, response):
    response.body = {'pattern_mvvm_dynamic_no_route': True}
    return response
