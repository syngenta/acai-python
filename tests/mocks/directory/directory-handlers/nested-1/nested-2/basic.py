def post(request, response):
    response.body = {'nested-2': True}
    return response
