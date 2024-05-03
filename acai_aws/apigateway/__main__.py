from acai_aws.apigateway.openapi_generator.handler.module import HandlerModule
from acai_aws.apigateway.openapi_generator.handler.scanner import HandlerScanner
from acai_aws.apigateway.openapi_generator.input.arguments import InputArguments
from acai_aws.apigateway.openapi_generator.input.validator import InputValidator


if __name__ == "__main__":
    inputs = InputArguments()
    validator = InputValidator()
    scanner = HandlerScanner(inputs.handlers)
    validator.validate_arguments(inputs)
    file_paths = scanner.get_handler_file_paths()
    result = HandlerModule.convert_from_file_paths(file_paths)
    print(result)