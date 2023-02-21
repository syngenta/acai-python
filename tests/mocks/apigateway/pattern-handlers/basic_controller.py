def post(request, response):
	response.body = {'basic-pattern': True}
	return response
