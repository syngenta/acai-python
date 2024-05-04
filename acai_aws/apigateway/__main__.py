from acai_aws.apigateway.openapi_generator.handler.importer import HandlerImporter
from acai_aws.apigateway.openapi_generator.handler.scanner import HandlerScanner
from acai_aws.apigateway.openapi_generator.input.arguments import InputArguments
from acai_aws.apigateway.openapi_generator.input.validator import InputValidator


if __name__ == "__main__":
    inputs = InputArguments()
    validator = InputValidator()
    scanner = HandlerScanner(inputs.handlers)
    importer = HandlerImporter()
    validator.validate_arguments(inputs)
    file_paths = scanner.get_handler_file_paths()
    results = importer.get_modules_from_file_paths(file_paths, scanner.handlers_base, inputs.base)
    for module in results:
        print(f'{module.file_path} => {module.method}::{module.route_path} -> {module.operation_id}')
