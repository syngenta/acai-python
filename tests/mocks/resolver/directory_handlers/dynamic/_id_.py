def post(request, response):
    response.body = {'directory_dynamic': True}
    return response
