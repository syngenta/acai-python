def post(_, response):
    response.body = {'mapping_home_init': True}
    return response
