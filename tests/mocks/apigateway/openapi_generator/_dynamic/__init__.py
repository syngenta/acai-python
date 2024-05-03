def post(_, response):
    response.body = {'dynamic': True}
    return response
