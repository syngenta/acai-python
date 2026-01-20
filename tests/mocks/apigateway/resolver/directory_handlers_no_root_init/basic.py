def post(request, response):
    response.body = {'directory_basic': True}
    return response
