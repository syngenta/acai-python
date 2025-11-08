# AGENTS.md

This repository contains **acai_aws**, a happy-path-first toolkit for AWS Lambda handlers. This guide distills the canonical documentation so another AI agent can navigate the codebase without digging through the docs.

## Philosophy & Environment
- Validate early, execute later. Every handler or event processor should assume inputs are clean because requirements and middleware already filtered the bad paths.
- Python 3.8+ is the baseline. Install dependencies via `pipenv install --dev` and use `pipenv run` to invoke tooling so the virtualenv stays consistent.
- Preferred workflow for any meaningful change: `pipenv run lint`, `pipenv run test`, `pipenv run coverage`, and—when request/response contracts change—`pipenv run generate` to refresh the OpenAPI spec.

## API Gateway Architecture
### Router Responsibilities
- The router owns request dispatch, validation, middleware orchestration, optional auth, and error handling. Core options include:
  - `base_path` (required) to match the API Gateway stage.
  - `handlers` (required) pointing to the directory that mirrors routes.
  - `schema` plus `auto_validate`/`validate_response` to wire OpenAPI checks.
  - `cors` (default `True`), `timeout`, `output_error`, `verbose_logging`, `cache_mode` (`all`, `static-only`, `dynamic-only`), and `cache_size` (default `128`).
  - Middleware hooks: `before_all`, `after_all`, `with_auth`, `on_error`, `on_timeout`.
- Always call `router.auto_load()` so directory traversal happens once during cold start. Dynamic imports are cached per the `cache_mode`/`cache_size` combination.

### File-System Routing Rules
- Directory names become path segments; `__init__.py` represents the index route for that segment.
- Files prefixed with `_` declare a path parameter: `_user_id.py` responds to `/users/{user_id}`. Keep the placeholder name identical to the suffix (`user_id`) so `request.path_params` stays intuitive.
- All HTTP verbs map to functions with lowercase names (`get`, `post`, etc.). Unsupported verbs simply don’t exist in the handler module.

### Middleware Order
1. `before_all`
2. Route-level `before` hook
3. Authentication via `with_auth` when `auth_required=True`
4. Handler function
5. Route-level `after` hook
6. `after_all`
7. Error/timeout hooks only if an exception bubbles up

Maintain this order whenever touching router internals; tests expect it.

## Handler Requirements & Validation
- Use `@requirements(...)` from `acai_aws.apigateway.requirements` to describe what makes a request valid. Supported keys include:
  - `required_headers`, `available_headers`
  - `required_query`, `available_query`
  - `required_route` for dynamic segments (e.g., `grower/{grower_id}`)
  - `required_body` and `required_response` referencing OpenAPI components or inline JSON Schema dicts
  - `auth_required` to trigger `with_auth`
  - `request_class` to swap in a custom request wrapper
  - `before`/`after` functions scoped to a single endpoint
  - `timeout` overrides (seconds, handler runtime only)
  - `summary`, `deprecated`, and arbitrary custom fields for OpenAPI generation or middleware hints
- All validation errors should flow through `response.set_error` so clients receive consistent payloads.

## Request & Response Contracts
- **Request** objects expose normalized HTTP metadata: `method`, `headers`, `query_params`, `path_params`, `route`, `path`, `cookies`, and `authorizer`. Body helpers auto-detect based on `Content-Type`:
  - `request.json`, `request.form`, `request.xml`, `request.graphql`, and `request.body` (auto-converts but falls back to raw data).
  - `request.raw` retains the unmodified payload.
  - `request.context` is the only mutable property—middleware can stash data here for later steps.
- **Response** objects provide:
  - `response.code` (default 200) and `response.headers` (tuples merged into a dict).
  - `response.body` with automatic JSON serialization.
  - `response.raw` to bypass serialization when `after`/`after_all` need to mutate the payload.
  - `response.compress` to gzip the final body.
  - `response.set_error(key, message)` and `response.has_error` for structured error responses.

## OpenAPI Generation
- Run `python -m acai_aws.apigateway generate-openapi --handlers=<glob> --base=<base_path> --output=<dir> --format=json,yml --delete` when handler requirements change. This command scans decorated functions, syncs paths/methods, and optionally prunes stale routes (`--delete`). Keep handler metadata descriptive so the generated doc is meaningful.

## Event Processors (Non-HTTP)
Every AWS event module follows the same shape: import `requirements` from the service package, decorate a handler, and iterate over normalized records.

| Service | Highlights |
|---------|------------|
| DynamoDB | Converts Dynamo JSON to native dicts, can filter by operations (`INSERT`, `MODIFY`, `REMOVE` or aliases), validates record bodies, supports `data_class` injection. |
| S3 | Optional `get_object` fetches the object body. `data_type` controls parsing (`json`, `csv`, or raw). Operations filters focus on create/update/delete events. |
| SQS/SNS | Normalizes message bodies to dicts, surfaces message attributes, and supports JSON Schema validation plus data classes. |
| Kinesis/Firehose/MSK/MQ | Batch processors built on `BaseRecordsEvent`; can apply schema validation and data classes per record, keeping streaming semantics intact. |
| DocumentDB | Tailored for change streams with access to `operationType`, full documents, and metadata. |
| Generic | Simplifies console/CLI-triggered events with body parsing and schema validation. |

Tips when editing event modules:
- Keep constructor signatures consistent so `event.records` always returns iterable record objects.
- Honor `operations` filters; when they’re misconfigured the event should no-op unless `raise_operation_error=True`.
- Data classes receive a `record` instance. Keep their API stable to avoid breaking user code.

## Logger & Observability
- `acai_aws.common.logger` logs structured JSON by default. Switching `LOG_FORMAT=INLINE` helps during local dev while `LOG_FORMAT=JSON` keeps CloudWatch-friendly output. `LOG_LEVEL` gates log emission (`INFO`, `DEBUG`, `WARN`, `ERROR`).
- The `@log` decorator wraps any function, optionally gating logs with a boolean `condition`. Maintain argument pass-through so debugging remains straightforward.
- Error traces should include the stack plus the high-level message; tests assert the JSON keys stay consistent (`level`, `time`, `error_trace`, `log`).

## Agent Checklist
1. **Understand the route or event** you’re touching—confirm how the filesystem maps to the API or which event module processes the payload.
2. **Update requirements first**, letting validation guardrails enforce behavior instead of branching in business logic.
3. **Keep Request/Response contracts untouched** unless there’s a strong reason; these are relied on by every handler.
4. **Mirror changes across services** when working inside shared abstractions like `BaseRecordsEvent`.
5. **Write or update tests** under `tests/acai_aws/...` that mirror the source layout.
6. **Run lint/tests/coverage/generate** (noted above) and capture any failures or skipped steps in your summary so humans can follow up.
7. **Document surprises**: if AWS quirks require deviations from the standard flow, leave concise comments or docstrings explaining the reason.

Following this guide keeps future agents aligned with Acai’s happy-path principles while minimizing regressions across API Gateway handlers and event processors alike.
