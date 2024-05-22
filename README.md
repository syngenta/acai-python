[![CircleCI](https://circleci.com/gh/syngenta/acai-python.svg?style=shield)](https://circleci.com/gh/syngenta/acai-python)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=syngenta_acai-python&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=syngenta_acai-python)

# Acai AWS
DRY, configurable, declarative node library for working with Amazon Web Service Lambdas.

## Features
* Highly configurable apigateway internal router
* Openapi schema adherence for all event types
* Generate OpenAPI docs from code base
* Extensible and customizable middleware for validation and other tasks
* DRY coding interfaces without the need of boilerplate
* Ease-of-use with the [serverless framework](https://www.serverless.com/)
* Local Development support
* Happy Path Programming (See Philosophy below)

## Philosophy

The Acai philosophy is to provide a dry, configurable, declarative library for use with the amazon lambdas, which encourages Happy Path Programming (HPP).

Happy Path Programming is an idea in which inputs are all validated before operated on. This ensures code follows the happy path without the need for mid-level, nested exceptions and all the nasty exception handling that comes with that. The library uses layers of customizable middleware options to allow a developer to easily dictate what constitutes a valid input, without nested conditionals, try/catch blocks or other coding blocks which distract from the happy path that covers the majority of that codes intended operation.

## Installation

This is a [python](https://www.python.org/) module available through the
[pypi registry](https://pypi.org).

Before installing, [download and install python](https://www.python.org/downloads/).
python 3 or higher is required.


Installation is done using the
[`pip install`](https://packaging.python.org/tutorials/installing-packages/) command:

```bash
$ pip install acai_aws
# pipenv install acai_aws
# poetry add acai_aws
```
## Documentation & Examples

* [Full Docs](https://syngenta.github.io/acai-python-docs/)
* [Tutorial](https://syngenta.github.io/acai-python-docs/)
* [Examples](https://github.com/syngenta/acai-python-docs/blob/main/examples/)


## Contributing

If you would like to contribute please make sure to follow the established patterns and unit test your code:

### Unit Testing

To run unit test, enter command:
```bash
$ pipenv install
$ pipenv run test
```
