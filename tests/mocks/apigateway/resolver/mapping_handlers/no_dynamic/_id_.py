def post(_, response):
    response.body = {'mapping_dynamic_no_route': True}
    return response
