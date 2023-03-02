def post(_, response):
    response.body = {'nested-2': True}
    return response
