def post(_, response):
    response.body = {'basic-directory': True}
    return response
