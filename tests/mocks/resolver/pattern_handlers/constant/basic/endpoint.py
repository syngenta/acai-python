def post(_, response):
    response.body = {'basic_constant_pattern': True}
    return response
