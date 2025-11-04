# CODEX.md

Codex, this repository houses **acai_aws**, a DRY toolkit for building AWS Lambda functions that receive API Gateway requests or batched records (DynamoDB, SQS, SNS, S3, Kinesis, MSK, MQ, Firehose, DocumentDB).

## Quick Start

- Install runtime and dev dependencies: `pipenv install --dev`
- Run the unittest discovery suite: `pipenv run test`
- Lint and coverage helpers: `pipenv run lint`, `pipenv run coverage`
- Generate OpenAPI docs: `pipenv run generate`

## Architecture Cheat Sheet

- `acai_aws/apigateway/router.Router` orchestrates requests: before/after hooks, optional auth, OpenAPI-driven validation, and error handling.
- Handlers declare requirements via `@acai_aws.apigateway.requirements.requirements(...)`—timeout, auth, schemas, hooks, and data classes.
- `acai_aws/apigateway/resolver` selects handler modules (directory/pattern/mapping); dynamic segments stay literal (hyphen safe).
- Record processors inherit `acai_aws.base.event.BaseRecordsEvent`; service-specific `Event`/`Record` classes live under `acai_aws/{service}/`.
- Validation flows through `acai_aws.common.validator.Validator`, backed by `jsonschema` or `pydantic` models.

## Testing Notes

- Tests mirror the package structure under `tests/acai_aws/`; mocks reside in `tests/mocks/`.
- Router tests assert full response dicts—double-check expected `path_params` when changing dynamic route handling.
- Coverage target lives in `pipenv run coverage` (pytest + coverage + HTML/JUnit reports).

## Tips While Editing

- Prefer `apply_patch` for manual edits; avoid auto-formatters unless explicitly requested.
- Keep responses JSON-serializable in router flows; `Response.body` defaults to JSON encoding.
- Dynamic route params may include hyphens—do **not** normalize to underscores; rely on segment-level import resolution instead.
- Many records expose `.operation`; filtering via `operations=[...]` occurs in `BaseRecordsEvent`.

## CI Expectations

- Lint score must remain ≥10 (`pipenv run lint`).
- Unit tests run via `pipenv run test` (unittest discovery).
- Publishing reads version from `CIRCLE_TAG`; avoid hardcoding.

Use this sheet to align with the repo’s conventions and keep happy-path programming intact.
