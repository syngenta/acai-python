def post(_, response):
    response.body = {'basic-pattern': True}
    return response
