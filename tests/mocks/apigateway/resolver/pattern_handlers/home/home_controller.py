def post(_, response):
    response.body = {'pattern_home_controller': True}
    return response
