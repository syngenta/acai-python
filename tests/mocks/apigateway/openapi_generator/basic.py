def post(_, response):
    response.body = {'basic-openapigenerator': True}
    return response
