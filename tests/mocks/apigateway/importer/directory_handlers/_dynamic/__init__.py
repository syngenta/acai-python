def post(_, response):
    response.body = {'dynamic-directory': True}
    return response
