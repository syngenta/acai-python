from acai_aws.apigateway.requirements import requirements


@requirements(
    required_body='v1-resource-body'
)
def put(_, response):
    response.body = {'nested-2-resource': True}
    return response
