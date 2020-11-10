from syngenta_digital_alc.apigateway.handler_requirements import handler_requirements

@handler_requirements()
def get(request, response):
    response.body = {
        'hello': 'world'
    }
