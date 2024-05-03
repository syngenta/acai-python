def post(_, response):
    response.body = {'nested-2-id': True}
    return response
