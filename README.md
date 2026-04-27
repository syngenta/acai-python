# 🫐 Acai AWS

## Auto-loading, self-validating, minimalist Python framework for Amazon Web Service Lambdas

[![CircleCI](https://circleci.com/gh/syngenta/acai-python.svg?style=shield)](https://circleci.com/gh/syngenta/acai-python)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=syngenta_acai-python&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=syngenta_acai-python)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=syngenta_acai-python&metric=bugs)](https://sonarcloud.io/summary/new_code?id=syngenta_acai-python)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=syngenta_acai-python&metric=coverage)](https://sonarcloud.io/summary/new_code?id=syngenta_acai-python)
[![Python](https://img.shields.io/pypi/pyversions/acai_aws.svg?color=blue)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/acai_aws?color=blue&label=PyPI)](https://pypi.org/project/acai_aws/)
[![License](https://img.shields.io/badge/license-apache2.0-blue)](LICENSE)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-blue.svg?style=flat)](https://github.com/syngenta/acai-python/issues)

A DRY, configurable, declarative Python library for working with AWS Lambdas that encourages **Happy Path Programming** — validate first, execute later — eliminating defensive try/except chains and tangled conditionals.

## 📖 Documentation

**[Full Documentation](https://syngenta.github.io/acai-python-docs/)** | **[Examples](https://github.com/syngenta/acai-python-docs/tree/main/examples)**

Learn how to wire API Gateway routes, validate payloads with OpenAPI or Pydantic, and process event-based services in the [Acai AWS docs](https://syngenta.github.io/acai-python-docs/).

---

## 🎯 Why Acai AWS?

Building Lambda functions shouldn’t require boilerplate or ad-hoc validation. Acai AWS provides:

- **🚀 Zero Boilerplate** – Auto-discover handlers based on directory, glob, or mapping modes
- **✅ Built-in Validation** – OpenAPI schema enforcement or Pydantic models with no extra glue code
- **🛡️ Declarative Requirements** – Decorators to plug in auth, before/after hooks, timeouts, and schema rules
- **🔄 Event Processing** – Consistent abstractions for DynamoDB Streams, SQS, S3, SNS, Kinesis, Firehose, MSK, MQ, DocumentDB, and ALB
- **🧪 Easy Testing** – Lightweight objects make unittest/pytest straightforward
- **⚙️ IDE-Friendly** – Intuitive, type-friendly request/response objects for a better developer experience

### Happy Path Programming Philosophy

Acai AWS embraces **Happy Path Programming (HPP)** — validate inputs upfront so business logic stays clean:

```python
# ❌ Without Acai AWS: Defend every line
def handler(event, _context):
    body = json.loads(event.get('body') or '{}')
    if 'email' not in body:
        return {"statusCode": 400, "body": '{"error": "Email required"}'}
    if not EMAIL_REGEX.match(body['email']):
        return {"statusCode": 400, "body": '{"error": "Invalid email"}'}
    # ... additional checks ...
    return {"statusCode": 200, "body": json.dumps(do_work(body))}
```

```python
# ✅ With Acai AWS: Validation is centralized
from acai_aws.apigateway.requirements import requirements

@requirements(required_body='v1-user-post-request')
def post(request, response):
    # request.body already validated
    response.body = {'userId': '123', 'email': request.body['email']}
    return response
```

---

## 📦 Installation

```bash
pip install acai_aws
# pipenv install acai_aws
# poetry add acai_aws
```

### Requirements

- **Python**: 3.8+
- **AWS SDK**: Optional, only needed for features like S3 object fetching (`boto3` is installed by default)

---

## 🚀 Quick Start

### API Gateway Router with Declarative Requirements

```python
# app.py (entry point for your Lambda)
from acai_aws.apigateway.router import Router


def authenticate(request, response, requirements):
    if request.headers.get('x-api-key') != 'secret-key':
        response.code = 401
        response.set_error('auth', 'Unauthorized')


router = Router(
    base_path='api/v1',
    handlers='handlers',            # directory mode
    schema='openapi.yml',           # optional OpenAPI document
    auto_validate=True,
    validate_response=True,
    with_auth=authenticate
)
router.auto_load()


def handler(event, context):
    return router.route(event, context)
```

```python
# handlers/users.py
from acai_aws.apigateway.requirements import requirements

@requirements(
    auth_required=True,
    required_body={ # can be a dataclass or reference to a schema in openapi.yml
        'type': 'object',
        'required': ['email', 'name'],
        'properties': {
            'email': {'type': 'string', 'format': 'email'},
            'name': {'type': 'string'}
        }
    }
)
def post(request, response):
    response.body = {
        'id': 'user-123',
        'email': request.body['email'],
        'name': request.body['name']
    }
    return response

def get(_request, response):
    response.body = {'users': []}
    return response
```

### Minimal Router Setup

```python
from acai_aws.apigateway.router import Router

router = Router(
    base_path='your-service/v1',
    handlers='api/handlers',
    schema='api/openapi.yml'
)
router.auto_load()

def handle(event, context):
    return router.route(event, context)
```

The router automatically maps file structure to routes (see the table in the [docs](https://syngenta.github.io/acai-python-docs/apigateway/quickstart/#minimal-setup)). For alternative modes—pattern globbing or explicit mappings—refer to the [configuration guide](https://syngenta.github.io/acai-python-docs/apigateway/configuration-details/).

```
~~ Directory ~~                     ~~ Route ~~
===================================================================
📦api/                              |
│---📂handlers                      |
    │---📜router.py                 |
    │---📜org.py                    | /org
    │---📂grower                    |
        │---📜__init__.py           | /grower
        │---📜_grower_id.py         | /grower/{grower_id}
    │---📂farm                      |
        │---📜__init__.py           | /farm
        │---📂_farm_id              |
            │---📜__init__.py       | /farm/{farm_id}
            │---📂field             |
                │---📜__init__.py   | /farm/{farm_id}/field
                │---📜_field_id.py  | /farm/{farm_id}/field/{field_id}
```

### ALB Router

`acai_aws.alb.Router` provides the same routing, validation, and middleware as the API Gateway router for Lambda functions invoked by an Application Load Balancer. It subclasses `apigateway.Router` and reuses the same handler files, `@requirements` decorator, OpenAPI auto-validation, and directory/mapping/pattern resolution — only the request/response transport differs.

```python
from acai_aws.alb.router import Router

router = Router(
    base_path='api/v1',
    handlers='handlers',
)
router.auto_load()

def handler(event, context):
    return router.route(event, context)
```

ALB-specific behavior layered on top of the apigateway router:

- **Base64 bodies** — when the ALB target group sends `isBase64Encoded: true`, `request.body` is transparently decoded.
- **`statusDescription`** — every response includes the `statusDescription` field ALB expects (e.g. `"200 OK"`, `"404 Not Found"`).
- **Request extras** — `request.target_group_arn` and `request.source_ip` (read from `x-forwarded-for`).

For records-style ALB processing (treating each invocation as a batch event rather than HTTP routing), see the [ALB section](#-event-processing) below.

### Auto-Loading OpenAPI Documents

```bash
pipenv run generate
# → loads handlers, inspects @requirements metadata, and updates openapi.yml/json
```

---

## 🔄 Event Processing

Acai AWS provides consistent event objects for AWS stream and queue services. Decorate your handler with `acai_aws.common.records.requirements.requirements` to auto-detect the source and wrap records.

```python
from acai_aws.dynamodb.requirements import requirements

class ProductRecord:
    def __init__(self, record):
        self.id = record.body['id']
        self.payload = record.body

@requirements(
    operations=['created', 'updated'],
    timeout=10,
    data_class=ProductRecord
)
def handler(records):
    for record in records.records:
        process_product(record.id, record.payload)
    return {'processed': len(records.records)}
```

Supported services include:

**DynamoDB Streams**

```python
from acai_aws.dynamodb.requirements import requirements as ddb_requirements

@ddb_requirements()
def dynamodb_handler(records):
    for record in records.records:
        handle_ddb_change(record.operation, record.body)
```

**Amazon SQS**

```python
from acai_aws.sqs.requirements import requirements as sqs_requirements

@sqs_requirements()
def sqs_handler(records):
    for record in records.records:
        handle_message(record.body, record.attributes)
```

**Amazon SNS**

```python
from acai_aws.sns.requirements import requirements as sns_requirements

@sns_requirements()
def sns_handler(records):
    for record in records.records:
        handle_notification(record.body, record.subject)
```

**Amazon S3**

```python
from acai_aws.s3.requirements import requirements as s3_requirements

@s3_requirements(get_object=True, data_type='json')
def s3_handler(records):
    for record in records.records:
        handle_object(record.bucket, record.key, record.body)
```

**Amazon Kinesis**

```python
from acai_aws.kinesis.requirements import requirements as kinesis_requirements

@kinesis_requirements()
def kinesis_handler(records):
    for record in records.records:
        handle_stream_event(record.partition_key, record.body)
```

**Amazon Firehose**

```python
from acai_aws.firehose.requirements import requirements as firehose_requirements

@firehose_requirements()
def firehose_handler(records):
    for record in records.records:
        handle_delivery(record.record_id, record.body)
```

**Amazon MSK**

```python
from acai_aws.msk.requirements import requirements as msk_requirements

@msk_requirements()
def msk_handler(records):
    for record in records.records:
        handle_msk_message(record.topic, record.body)
```

**Amazon MQ**

```python
from acai_aws.mq.requirements import requirements as mq_requirements

@mq_requirements()
def mq_handler(records):
    for record in records.records:
        handle_mq_message(record.message_id, record.body)
```

**Amazon DocumentDB Change Streams**

```python
from acai_aws.documentdb.requirements import requirements as docdb_requirements

@docdb_requirements()
def docdb_handler(records):
    for record in records.records:
        handle_docdb_change(record.operation, record.full_document)
```

**Application Load Balancer (ALB)**

```python
from acai_aws.alb.requirements import requirements as alb_requirements

@alb_requirements()
def alb_handler(records):
    for record in records.records:
        handle_request(record.http_method, record.body, record.source_ip)
```

Each record exposes intuitive properties like `record.operation`, `record.body`, or service-specific metadata (bucket, partition, headers, etc.).

### Validating Record Bodies with Pydantic or JSON Schema

Records events (SQS, Kinesis, DynamoDB, SNS, S3, MSK, MQ, Firehose, DocumentDB, ALB) accept the same `required_body` validation as API Gateway — either a JSON Schema dict, an OpenAPI component name string, or a Pydantic `BaseModel` subclass.

```python
from pydantic import BaseModel
from acai_aws.sqs.requirements import requirements

class OrderEvent(BaseModel):
    order_id: str
    amount: float

@requirements(required_body=OrderEvent)
def handler(event):
    for record in event.records:  # invalid records filtered before this loop
        process(record.body)
```

### Controlling Validation Failure Behavior with `failure_mode`

By default, invalid records are silently filtered out of `event.records` — preserving existing behavior. Opt into louder modes with `failure_mode` (also controls the `operations=[...]` filter).

```python
from acai_aws.base.event import FailureMode
```

| Mode | Behavior |
|---|---|
| `FailureMode.SILENT_IGNORE` (default) | Invalid records dropped silently. Handler receives only valid records. |
| `FailureMode.LOG_WARN` | Invalid records dropped **and** each failure emitted as a structured WARN log entry. |
| `FailureMode.RAISE_ERROR` | First invalid record raises `RecordException` immediately, before the handler runs. Replaces the deprecated `raise_body_error=True` / `raise_operation_error=True` booleans. |
| `FailureMode.RETURN_FAILURE` | Invalid records collected on `event.invalid_records`. After the handler returns, the decorator auto-merges framework-detected failures into the response's `batchItemFailures` list (SQS/Kinesis/DynamoDB) — compatible with AWS Lambda partial batch response. |

#### Auto-hydrated `batchItemFailures` for SQS, Kinesis, DynamoDB

When `failure_mode=FailureMode.RETURN_FAILURE` is set on a source that supports partial batch response, the framework merges its detected failures into whatever your handler returns — letting the event-source mapping retry malformed messages correctly instead of silently dropping them.

```python
from pydantic import BaseModel
from acai_aws.base.event import FailureMode
from acai_aws.sqs.requirements import requirements

class OrderEvent(BaseModel):
    order_id: str
    amount: float

@requirements(required_body=OrderEvent, failure_mode=FailureMode.RETURN_FAILURE)
def handler(event):
    handler_failures = []
    for record in event.records:  # only valid records
        try:
            process(record.body)
        except TransientError:
            handler_failures.append({'itemIdentifier': record.message_id})
    return {'batchItemFailures': handler_failures}
    # Framework appends validation failures to batchItemFailures automatically.
    # SQS retries both kinds. No silent data loss.
```

Per-source identifiers used by the auto-merge:

| Source | `itemIdentifier` |
|---|---|
| SQS | `record.message_id` |
| Kinesis | `record.sequence_number` |
| DynamoDB Streams | `record.sequence_number` |
| MSK | `f'{record.topic}-{record.partition}-{record.offset}'` |

Sources without partial-batch support (SNS, S3, Firehose, MQ, DocumentDB) fall back to `SILENT_IGNORE` semantics for `RETURN_FAILURE` — use `LOG_WARN` for those instead.

#### ALB: Automatic HTTP 400 on Invalid Body

ALB is synchronous HTTP — partial-batch semantics don't apply. When `required_body` is set on an ALB handler and the body fails validation, the framework **short-circuits the handler** and returns an HTTP 400 response in the same shape API Gateway produces:

```json
{
  "statusCode": 400,
  "headers": {"Content-Type": "application/json"},
  "body": "{\"errors\": [{\"key_path\": \"amount\", \"message\": \"Input should be a valid number\"}]}",
  "isBase64Encoded": false
}
```

```python
from acai_aws.alb.requirements import requirements

@requirements(required_body=OrderEvent)
def alb_handler(event):
    # Only runs when the body validates. Otherwise framework returns 400.
    return {'statusCode': 200, 'body': '{"ok": true}'}
```

#### Deprecation: `raise_body_error` / `raise_operation_error`

The old `raise_body_error=True` and `raise_operation_error=True` kwargs still work and translate to `failure_mode=FailureMode.RAISE_ERROR`, but emit a deprecation warning. Prefer the unified enum going forward.

---

## 🧰 Tooling & Development Experience

- **OpenAPI Generator** – CLI (`python -m acai_aws.apigateway generate-openapi`) scans handlers and updates schema docs
- **Request/Response Helpers** – Access JSON, GraphQL, form, XML, or raw bodies via `Request.json`, `Request.form`, etc.
- **Logging** – Configurable JSON/inline logging via `acai_aws.common.logger`
- **Validation** – JSON Schema (Draft 7) and Pydantic support with helpful error messages

---

## 🧪 Testing

```bash
pipenv install --dev
pipenv run test         # run unittest discovery
pipenv run coverage     # run pytest suite with coverage reports
pipenv run lint         # run pylint with bundled rules
```

### Example Unit Test

```python
import json
from unittest import TestCase

from acai_aws.apigateway.router import Router

class UsersEndpointTest(TestCase):
    def setUp(self):
        self.router = Router(base_path='api/v1', handlers='tests/handlers')

    def test_creates_user(self):
        event = {
            'path': 'api/v1/users',
            'httpMethod': 'POST',
            'headers': {'content-type': 'application/json'},
            'body': json.dumps({'email': 'unit@example.com', 'name': 'Unit'})
        }
        result = self.router.route(event, None)
        payload = json.loads(result['body'])

        self.assertEqual(200, result['statusCode'])
        self.assertEqual('unit@example.com', payload['email'])
```

---

## 🤝 Contributing

Contributions welcome! Follow the usual GitHub flow:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-idea`)
3. Write tests and code (`pipenv run test`)
4. Run linting (`pipenv run lint`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/syngenta/acai-python.git
cd acai-python
pipenv install --dev
pipenv run test
pipenv run lint
```

---

## 📄 License

Apache 2.0 © [Paul Cruse III](https://github.com/paulcruse3)

---

## 🙏 Acknowledgments

Acai AWS continues the Happy Path philosophy introduced in [acai-js](https://github.com/syngenta/acai-js) and expanded by [Acai-TS](https://github.com/syngenta/acai-ts). Thanks to the original contributors who made Lambda development less painful.

---

## 💬 Support & Community

- **📖 Documentation**: [https://syngenta.github.io/acai-python-docs/](https://syngenta.github.io/acai-python-docs/)
- **💻 Examples**: [https://github.com/syngenta/acai-python-docs/tree/main/examples](https://github.com/syngenta/acai-python-docs/tree/main/examples)
- **🐛 Issues**: [GitHub Issues](https://github.com/syngenta/acai-python/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/syngenta/acai-python/discussions)

Made with 💙 by developers who believe AWS Lambda development should be enjoyable.
