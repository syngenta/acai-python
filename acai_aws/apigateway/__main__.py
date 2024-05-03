from acai_aws.apigateway.openapi_generator.input.arguments import InputArguments
from acai_aws.apigateway.openapi_generator.input.validator import InputValidator
from acai_aws.apigateway.openapi_generator.handler.scanner import HandlerScanner


if __name__ == "__main__":
    inputs = InputArguments()
    validator = InputValidator()
    scanner = HandlerScanner(inputs.handlers)
    validator.validate_arguments(inputs)
    result = scanner.get_handler_modules()
    print(result)