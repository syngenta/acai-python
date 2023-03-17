class Validator:

    def __init__(self):
        self.__pairings = {
            'required_headers': 'headers',
            'available_headers': 'headers',
            'required_query': 'query_params',
            'available_query': 'query_params'
        }

    def validate_request(self, request, response, requirements):
        for required, source in self.__pairings.items():
            if requirements.get(required) and 'required' in required:
                Validator.required_fields(response, requirements[required], getattr(request, source), source)
            elif requirements.get(required) and 'available' in required:
                Validator.available_fields(response, requirements[required], getattr(request, source), source)

    @staticmethod
    def required_fields(response, required, sent, list_name=''):
        sent_keys = []
        if isinstance(sent, dict) and len(sent.keys()) > 0:
            sent_keys = sent.keys()
        missing_fields = [value for value in required if value not in sent_keys]
        if len(required) > 0:
            for field in missing_fields:
                response.code = 400
                response.set_error(list_name, f'Please provide {field} in {list_name}')

    @staticmethod
    def available_fields(response, available, sent, list_name=''):
        if len(available) > 0:
            unavailable_fields = [value for value in sent if value not in available]
            for field in unavailable_fields:
                response.code = 400
                response.set_error(list_name, f'{field} is not an available {list_name}')
