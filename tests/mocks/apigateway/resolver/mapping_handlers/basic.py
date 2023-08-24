def post(_, response):
    response.body = {'mapping_basic': True}
    return response
