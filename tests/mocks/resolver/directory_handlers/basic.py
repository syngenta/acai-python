def post(request, response):
    response.body = {'basic-directory': True}
    return response
