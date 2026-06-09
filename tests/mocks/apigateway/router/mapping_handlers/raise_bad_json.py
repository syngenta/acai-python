import json

from acai_aws.apigateway.requirements import requirements


@requirements()
def post(request, response):
    # A handler parsing JSON itself (e.g. a nested payload) hits a decode error
    # on malformed input; that is a client contract error, not a server fault.
    json.loads('{not valid json')
    return response
