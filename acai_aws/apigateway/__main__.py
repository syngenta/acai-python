import pprint
from icecream import ic

from acai_aws.apigateway.openapi.handler.importer import HandlerImporter
from acai_aws.apigateway.openapi.handler.scanner import HandlerScanner
from acai_aws.apigateway.openapi.input.arguments import InputArguments
from acai_aws.apigateway.openapi.input.validator import InputValidator
from acai_aws.apigateway.openapi.generator import OpenAPIGenerator
from acai_aws.apigateway.openapi.file_writer import OpenAPIFileWriter


def generate_openapi():
    inputs = InputArguments()
    validator = InputValidator()
    scanner = HandlerScanner(inputs.handlers)
    importer = HandlerImporter()
    generator = OpenAPIGenerator(inputs.output)
    writer = OpenAPIFileWriter()

    validator.validate_arguments(inputs)
    file_paths = scanner.get_handler_file_paths()
    modules = importer.get_modules_from_file_paths(file_paths, scanner.handlers_base, inputs.base)

    for module in modules:
        generator.add_path_and_method(module)

    if inputs.delete:
        generator.delete_unused_paths()

    writer.write_openapi(generator.doc, inputs.output, inputs.formats)


if __name__ == '__main__':  # pragma: no cover
    generate_openapi()
