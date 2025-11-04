# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**acai_aws** is a DRY, configurable, declarative Python library for working with Amazon Web Services Lambdas. It provides:
- Highly configurable API Gateway internal routing
- OpenAPI schema adherence and generation
- Extensible middleware for validation
- Support for multiple AWS event sources (S3, DynamoDB, Kinesis, SNS, SQS, MSK, MQ, DocumentDB, Firehose)
- Happy Path Programming (HPP) philosophy - inputs validated before operations

## Common Commands

### Development Environment
```bash
# Install dependencies (using pipenv)
pipenv install

# Install development dependencies
pipenv install --dev
```

### Testing
```bash
# Run all tests
pipenv run test

# Run with coverage report
pipenv run coverage
```

### Linting
```bash
# Run pylint with custom rules
pipenv run lint
```

### OpenAPI Generation
```bash
# Generate OpenAPI docs from handlers
pipenv run generate
# This generates OpenAPI documentation from handler files in tests/mocks/apigateway/openapi/**/*.py
```

### Running Single Tests
```bash
# Run specific test file
python -m unittest tests.acai_aws.<module>.<test_file>

# Example:
python -m unittest tests.acai_aws.apigateway.test_router
```

## Architecture Overview

### Core Philosophy: Happy Path Programming (HPP)
All inputs are validated before being operated on. The library uses layers of customizable middleware to allow developers to dictate valid inputs without nested conditionals or try/catch blocks.

### Module Structure

The codebase is organized by AWS service event types:

#### Event Handler Pattern
All event handlers follow a common inheritance pattern from `acai_aws.base.event.BaseRecordsEvent`:

```
BaseRecordsEvent (base/event.py)
├── DynamoDBEvent (dynamodb/event.py)
├── S3Event (s3/event.py)
├── KinesisEvent (kinesis/event.py)
├── SNSEvent (sns/event.py)
├── SQSEvent (sqs/event.py)
├── MSKEvent (msk/event.py)
├── MQEvent (mq/event.py)
├── DocumentDBEvent (documentdb/event.py)
└── FirehoseEvent (firehose/event.py)
```

Each event class:
1. Inherits from `BaseRecordsEvent`
2. Sets `self._record_class` to its specific Record class
3. Implements `records` property that returns validated, parsed records
4. Supports optional `data_class` for custom data transformations

#### API Gateway Architecture

The API Gateway module (`acai_aws/apigateway/`) provides a complete routing and validation system:

**Key Components:**
- `Router` - Main routing orchestrator with middleware pipeline
- `Request` - Normalized request object with multi-format body parsing (JSON, XML, form, GraphQL)
- `Response` - Response builder with error tracking
- `Endpoint` - Wrapper around handler functions with requirements metadata
- `Resolver` - Maps incoming requests to handler functions (supports directory and pattern-based routing)
- `Validator` - Request/response validation against OpenAPI specs or inline schemas

**Router Middleware Pipeline:**
1. `before_all` - Pre-processing hook
2. `with_auth` - Authentication/authorization
3. Request validation (OpenAPI or requirements-based)
4. Handler execution
5. Response validation (optional)
6. `after_all` - Post-processing hook
7. Error handling (`on_error`, `on_timeout`)

**Handler Requirements Decorator:**
Handlers use the `@requirements()` decorator to declare validation rules:

```python
from acai_aws.apigateway.requirements import requirements

@requirements(
    auth_required=True,
    required_headers=['x-api-key'],
    required_query=['user_id'],
    required_body={'$ref': '#/components/schemas/User'},
    timeout=30,
    before=pre_hook,
    after=post_hook
)
def post(request, response):
    response.body = {'result': 'success'}
    return response
```

#### Common Utilities

**Validator** (`acai_aws/common/validator.py`):
- Supports JSON Schema (Draft 7) and Pydantic model validation
- Validates request headers, query params, and body
- Validates response schemas
- Used by both API Gateway and event record validation

**Schema** (`acai_aws/common/schema.py`):
- Manages OpenAPI spec loading and reference resolution
- Extracts route specifications for validation

**JSON Helper** (`acai_aws/common/json_helper.py`):
- Handles JSON encoding/decoding with DynamoDB JSON format support

### Testing Structure

Tests mirror the source structure under `tests/acai_aws/`:
- Each module has corresponding test files
- Mocks are in `tests/mocks/` organized by service
- Mock functions demonstrate handler patterns

### OpenAPI Generation

The `apigateway` module includes a CLI tool for generating OpenAPI documentation from handler code:
- Scans handler files for decorated functions
- Extracts requirements metadata
- Generates/updates OpenAPI spec files in JSON/YAML
- Invoked via: `python -m acai_aws.apigateway generate-openapi`

## Code Style

### Linting Rules (from .pylintrc)
- Max line length: 140 characters
- String quotes: single quotes for strings, double quotes for docstrings
- Pylint score must be >= 10 to pass CI
- Private attributes use double underscore: `self.__attribute`
- Protected attributes use single underscore: `self._attribute`

### Naming Conventions
- Functions: `snake_case` (min 3 chars)
- Variables: `snake_case` (min 3 chars)
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Methods: `snake_case` (min 3 chars)

## CI/CD

### CircleCI Pipeline
- Python 3.9 environment
- Automated testing with coverage reports
- Pylint execution with score thresholds
- SonarCloud integration for code quality
- PyPI deployment on git tags

### Deployment
Package is deployed to PyPI automatically on tagged releases. Version is read from `CIRCLE_TAG` environment variable.

## Working with Events

### Record-based Event Handlers
When creating handlers for AWS event sources:

1. **Validation Options:**
   - `operations`: Filter by operation type (e.g., `['INSERT', 'MODIFY']` for DynamoDB)
   - `raise_operation_error`: Raise exception if operation doesn't match
   - `required_body`: JSON schema for record body validation
   - `raise_body_error`: Raise exception if body validation fails

2. **Data Classes:**
   - Set `event.data_class = YourDataClass` to transform records
   - Data class receives `record` parameter in constructor
   - `event.records` returns list of data class instances

3. **S3-Specific Features:**
   - `get_object=True`: Automatically fetch S3 object bodies
   - `data_type='json'|'csv'`: Parse object contents
   - `delimiter=','`: CSV delimiter (default: comma)

### API Gateway Handlers

1. **File-based Routing:**
   - Directory structure maps to routes: `handlers/user/_user_id.py` → `/user/{user_id}`
   - Pattern-based: `_param` becomes `{param}` path parameter
   - Method name matches HTTP method: `def get(request, response)`

2. **Request Object:**
   - Auto-detects content type and parses body
   - Access via: `request.body`, `request.json`, `request.xml`, `request.form`, `request.graphql`
   - Path params: `request.path_params['user_id']`
   - Query params: `request.query_params['filter']`

3. **Response Object:**
   - Set body: `response.body = {'data': 'value'}`
   - Set status: `response.code = 201`
   - Add errors: `response.set_error('field', 'error message')`
   - Check errors: `response.has_errors`

## Dependencies

Core dependencies:
- `boto3` - AWS SDK
- `jsonschema` - JSON Schema validation
- `pydantic` - Data validation with type hints
- `dynamodb_json` - DynamoDB JSON format handling

Development dependencies:
- `pytest` - Testing framework
- `pylint` - Linting
- `moto` - AWS service mocking
