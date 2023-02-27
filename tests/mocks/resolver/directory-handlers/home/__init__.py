def post(request, response):
    response.body = {'home': True}
    return response
