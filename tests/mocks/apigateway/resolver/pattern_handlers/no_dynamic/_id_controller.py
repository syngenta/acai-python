def post(_, response):
    response.body = {'pattern_dynamic_no_route': True}
    return response
