def post(_, response):
    response.body = {'nested-id': True}
    return response
