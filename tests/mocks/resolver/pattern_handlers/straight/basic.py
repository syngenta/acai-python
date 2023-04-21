def post(_, response):
    response.body = {'basic_straight_pattern': True}
    return response
