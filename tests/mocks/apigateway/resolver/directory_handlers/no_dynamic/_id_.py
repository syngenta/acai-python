
def post(request, response):
    response.body = {'directory_dynamic_no_route': True}
    return response
