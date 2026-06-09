from pydantic import BaseModel

from acai_aws.apigateway.requirements import requirements


class _OwnerModel(BaseModel):
    phone: str


@requirements()
def post(request, response):
    response.body = {'router_mapping_basic': request.body}
    # Missing required 'phone' raises pydantic ValidationError (v1 and v2),
    # mirroring a handler building a request model from a bad body.
    _OwnerModel()
    return response
