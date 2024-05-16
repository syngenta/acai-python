import json
import yaml


class OpenAPIFileWriter:

    def write_openapi(self, doc, file_location, formats):
        for write_format in formats:
            if write_format == 'json':
                self.__write_json(doc, file_location)
            if write_format == 'yml':
                self.__write_yml(doc, file_location)
    
    def __write_json(self, doc, file_locaiton):
        with open(f'{file_locaiton}/openapi.json', 'w') as openapi_json:
            openapi_json.write(json.dumps(doc, indent=4))

    def __write_yml(self, doc, file_locaiton):
        with open(f'{file_locaiton}/openapi.yml', 'w') as openapi_yml:
            yaml.dump(doc, openapi_yml, indent=4, default_flow_style=False, sort_keys=False)
        
    