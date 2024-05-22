from acai_aws.apigateway.router import Router


router = Router(
    base_path='your-service/v1',
    handlers='api/handlers',
    schema='api/openapi.yml'
)
router.auto_load()

def route(event, context):
    return router.route(event, context)