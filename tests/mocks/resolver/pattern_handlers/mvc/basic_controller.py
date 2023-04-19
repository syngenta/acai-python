def post(_, response):
    response.body = {'basic_mvc_pattern': True}
    return response
