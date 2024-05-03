def post(request, response):
    response.body = {'nested-2-resource': True}
    return response
