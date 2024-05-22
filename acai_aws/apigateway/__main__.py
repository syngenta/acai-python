import pprint
from icecream import ic

from acai_aws.apigateway.openapi.handler.importer import HandlerImporter
from acai_aws.apigateway.openapi.handler.scanner import HandlerScanner
from acai_aws.apigateway.openapi.input.arguments import InputArguments
from acai_aws.apigateway.openapi.input.validator import InputValidator
from acai_aws.apigateway.openapi.generator import OpenAPIGenerator
from acai_aws.apigateway.openapi.file_writer import OpenAPIFileWriter


def generate_openapi():
    print('STARTED')
    print('generating openapi docs...')
    print('validating arguments received...')
    inputs = InputArguments()
    validator = InputValidator()
    scanner = HandlerScanner(inputs.handlers)
    importer = HandlerImporter()
    generator = OpenAPIGenerator(inputs.output)
    writer = OpenAPIFileWriter()

    validator.validate_arguments(inputs)
    print('arguments validated...')
    file_paths = scanner.get_handler_file_paths()
    print(f'scanning handlers: {inputs.handlers}...')
    modules = importer.get_modules_from_file_paths(file_paths, scanner.handlers_base, inputs.base)
    print('importing handler endpoint modules...')

    for module in modules:
        generator.add_path_and_method(module)

    if inputs.delete:
        print('deleting paths and methods not found in code base')
        generator.delete_unused_paths()

    print(f'writing openapi doc to requested directory: {inputs.output}')
    writer.write_openapi(generator.doc, inputs.output, inputs.formats)
    print('COMPLETED')


if __name__ == '__main__':  # pragma: no cover
    generate_openapi()
