def post(request, response):
    response.body = {'dynamic': 1}
    return response
