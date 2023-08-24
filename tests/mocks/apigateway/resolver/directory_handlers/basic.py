def post(_, response):
    response.body = {'directory_basic': True}
    return response
