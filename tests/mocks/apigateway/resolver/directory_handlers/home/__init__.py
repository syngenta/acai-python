def post(request, response):
    response.body = {'directory_home': True}
    return response
