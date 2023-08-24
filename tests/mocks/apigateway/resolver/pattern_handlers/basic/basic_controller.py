def post(_, response):
    response.body = {'basic_pattern': True}
    return response
