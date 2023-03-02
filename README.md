# Syngenta Digital ALC (AWS Lambda Client)
Auto-loading, self-validating, minimalist python framework for AWS Lambdas

## Features

  * Automatic routing based on folder structure
  * Remove unnecessary boilerplate from your development process
  * Ease-of-use with the [serverless framework](https://www.serverless.com/)
  * Local development support

## Philosophy

The alc philosophy is to provide a self evident tool for use with amazon lambdas.

The alc encourages you to use small, internally routed API lambdas in a normalized OOP way.

In addition, it makes things like routing and validating API requests less cumbersome and time consuming.

## Installation

This is a [python](https://www.python.org/) module available through the
[pypi registry](https://pypi.org).

Before installing, [download and install python](https://www.python.org/downloads/).
python 3 or higher is required.


Installation is done using the
[`pip install`](https://packaging.python.org/tutorials/installing-packages/) command:

```bash
$ pip install acai
```

or

```bash
$ pipenv install acai
```

## Basic Usage

### apigateway events

`NOTE`: This packages assumes you are using a monolithic, internally routed lambda with [serverless framework](https://www.serverless.com/) and you have a folder structure which puts all your endpoint files in one sub directory tied to a custom domain on apigateway.

0. Setting Up the Monolithic Internally Routed Lambda

```yml
functions:
    v1-apigateway-handler:
        handler: application.v1.handler.apigateway._router.route
        events:
            - http:
                path: /v1/
                method: ANY
            - http:
                path: /v1/{proxy+}
                method: ANY    
```

1. Initialize the Router

```python
import os

from acai.apigateway.router.router import Router


# must pass current service, version of API and where handlers are located
def route(event, context):
    router = Router(
        base_path='{}/{}'.format(os.environ['service'], 'v1'),
        handler_path='application.v1.controller.apigateway',
        schema_path='application/openapi.yml',
        event=event,
        context=context
    )
    return router.route()

# examples of how router routes (called route -> will import):
# api.url.com/service/v1 -> application.v1.handler.apigateway.__init__.py
# api.url.com/service/v1/hello -> application.v1.handler.apigateway.hello.py
# api.url.com/service/v1/hello-world -> application.v1.handler.apigateway.hello_world.py

# @NOTE: router will always match HTTP Method with function name
# @NOTE: router does NOT support path parameters (please use query strings)
```

Option Name   | Required | Type   | Default | Description
:-----------  | :------- | :----- | :------ | :----------
`event`       | true     | dict   | n/a     | event object passed into lambda
`base_path`   | true     | string | n/a     | apigateway base path for the custom domain
`handler_path`| true     | string | n/a     | project path of where the endpoint files
`schema_path` | false    | string | null    | path where your schema file can found (accepts JSON as well)
`before_all`  | false    | string | null    | before all middleware function to run before all routes (after validation occurs)
`after_all`   | false    | string | null    | after all middleware function to run after all routes

2. Create handler file with matching methods and requirements

```python
from acai.apigateway.handler_requirements import handler_requirements


@handler_requirements(
    required_headers=['x-login-token', 'x-permission-token'],
    available_headers=['id', 'overwrite'],
    required_params=['id', 'overwrite'],
    available_params=['id', 'overwrite'],
    required_body='v1-post-example-request'
)
def post(request, response):
    response.body = business_layer.some_function(request.body)
    response.code = 201
```

***Endpoint Requirement Options***

Option Name        | Type   | Description
:-----------       | :----- | :----------
`required_body`    | string | the components schema key name
`available_params` | list   | list of available query string params for that method on that endpoint
`required_params`  | list   | list of required query string params for that method on that endpoint
`available_headers`| list   | list of available headers for that method on that endpoint
`required_headers` | list   | list of required headers for that method on that endpoint


***Request Properties***

Property Name       | Description
:-----------        | :-------   
`method`            | method id of apigateway event
`resource`          | resource handle of apigateway event
`authorizer`        | authorizer of apigateway event (will default to use headers if using with [serverless offline](https://www.npmjs.com/package/serverless-offline))
`headers`           | headers of apigateway event
`params`            | query string params of apigateway event
`path`              | path arguments of apigateway event
`json`              | body of apigateway event parsed as JSON
`graphql`           | body of apigateway event parsed as graphl (output is a graphql standard dict {query: 'some_graph_query{}'})
`form_encoded`      | body of apigateway event parsed from a form encoded string
`body`              | body of apigateway event will try to parse based on request headers, use a specific property (json, graphql, etc)if you know what you know the type of the request you're getting
`request`           | full request broken down as an dictionary


***Response Properties***

Property Name       | Description
:-----------        | :-------   
`headers`           | headers you want to send in response
`code`              | status code of response (will default to 204 if no content && will default 400 if errors found in response)
`authorizer`        | authorizer of apigateway event (will default to use headers if using with [serverless offline](https://www.npmjs.com/package/serverless-offline))
`base64_encoded`    | whether your body is base64Encoded [see docs](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format)
`compress`          | if set to true, will automatically compress, json and b64 encode as well as compress the body of your response and add appropriate headers
`has_errors()`      | function will tell you if errors in the response
`set_error()`       | function will set error key and message

***(OPTIONAL) RUN LOGIC BEFORE EVERY REQUEST***

This is a feature which allows you to interrogate all requests before they hit your endpoint. Here are some things to remember:

* your function will run only after a valid route and method have been determined
* runs before any validation
* requires you use the `BeforeAllException` class to stop processing or route will continue
* must be a pure function that is passed in context

#### Example configuration

```python
import os

from acai.apigateway.router.router import Router

from example.function.to. import
import example_before_all


def route(event, context):
    router = Router(
        base_path='{}/{}'.format(os.environ['service'], 'v1'),
        handler_path='application.v1.controller.apigateway',
        schema_path='application/openapi.yml',
        event=event,
        context=context,
        before_all=example_before_all.run  # this is the important part
    )
    return router.route()   
```

#### Example before all function

```python
from acai.apigateway.custom_exceptions import BeforeAllException
from acai.apigateway.handler_requirements import handler_requirements


@handler_requirements()
def run(request, response):
    if not request.headers.get('x-api-key') == 'some-secret-key':
        raise BeforeAllException(code=401, key_path='headers:x-api-key', message='you need an api key')

```

### sqs events

0. Setting Up your lambda to listen to the Queue

```yml
functions:
    v1-sqs-subscription:
        name: v1-sqs-subscription
        handler: application.v1.handler.sqs.listener.listen
        events:
            - sqs:
                arn:
                    Fn::GetAtt: [ ExampleQueue, 'Arn' ]
```

1. Initialize the Event and Iterate over the Records

```python
from acai.sqs.handler_requirements import handler_requirements


@handler_requirements()
def handle_sqs_trigger(event):
    records = event.records
    for sqs_record in records:
        some_func(sqs_record)
```

***Event Client Properties***

Property Name   | Description
:-----------    | :-------   
`records`       | list of record objects
`raw_records`   | jus the raw record from the original request


***Record Properties***

Property Name       | Description
:-----------        | :-------   
`message_id`        | message id of sqs record
`receipt_handle`    | receipt handle of sqs record
`body`              | body of sqs record (will automatically decode JSON)
`raw_body`          | body of sqs record
`attributes`        | attributes of sqs record
`message_attributes`| message attributes of sqs record
`md5_of_body`       | md5 of body of sqs record
`source`            | source of sqs record
`source_arn`        | source ARN of sqs record
`region`            | region of sqs record

### dynamodb events

0. Setting Up your lambda to listen to the dynamodb streams

```yml
functions:
    v1-dynamodb-stream:
        name: v1-dynamodb-stream
        handler: application.v1.handler.dynamodb.streamer.stream
        events:
            - stream:
                type: dynamodb
                arn:
                    Fn::GetAtt: [ DynamoDbTableExample, 'Arn' ]
```

1. Initialize the Event and Iterate over the Records

```python
from acai.dynamodb.handler_requirements import handler_requirements


@handler_requirements()
def handle_ddb_trigger(event):
    records = event.records
    for ddb_record in records:
        some_func(ddb_record)
```

***Event Client Properties***

Property Name   | Description
:-----------    | :-------   
`records`       | list of record objects
`raw_records`   | jus the raw record from the original request


***Record Properties***

Property Name                  | Description
:-----------                   | :-------   
`event_id`                     | event id of dynamodb record
`event_name`                   | event name of dynamodb record
`event_source`                 | event source  of dynamodb record
`keys`                         | keys of dynamodb record (will convert ddb json)
`old_image`                    | old image of dynamodb record
`new_image`                    | new image of dynamodb record
`raw_body`                     | raw of body of dynamodb record
`event_source_arn`             | event source ARN of dynamodb record
`event_version`                | event version of dynamodb record
`stream_view_type`             | stream view type version of dynamodb record
`size_bytes`                   | size bytes of dynamodb record
`approximate_creation_datetime`| approximate creation date time of dynamodb record


### s3 events

0. Setting Up your lambda to listen to s3 bucket changes

```yml
functions:
    v1-s3-handler:
        name: v1-s3-handler
        handler: application.v1.handler.s3.handler.handle
        events:
            - s3: photos
```

1. Initialize the Event and Iterate over the Records

```python
from acai.s3.handler_requirements import handler_requirements


@handler_requirements()
def handle_s3_trigger(event):
    records = event.records
    for s3_record in records:
        some_func(s3_record)
```

***Event Client Properties***

Property Name   | Description
:-----------    | :-------   
`records`       | list of record objects
`raw_records`   | jus the raw record from the original request


***Record Properties***

Property Name                 | Description
:-----------                  | :-------   
`event_time`                  | event time of s3 record
`event_name`                  | event name of s3 record
`event_source`                | event source  of s3 record
`region`                      | region of s3 record (will convert ddb json)
`request_parameters`          | request parameters of s3 record
`response_elements`           | response elements of s3 record
`s3_configuration_id`         | configuration id of s3 record
`s3_object`                   | object of s3 record
`s3_bucket`                   | bucket of s3 record
`s3_key`                      | key of the object for the s3 record
`s3_schema_version`           | s3 schema version of s3 record

### generic events

0. Setting Up your lambda to listen to take in random events

```yml
functions:
    v1-generic-handler:
        name: v1-generic-handler
        handler: application.v1.handler.console.handler.handle
```

1. Initialize the Event and Iterate over the Records

```python
from acai.generic.handler_requirements import handler_requirements


@handler_requirements()
def handle_generic_trigger(event):
    some_func(event.body)  # will automatically decode JSON, if it is JSON
```

***Event Client Properties***

Property Name   | Description
:-----------    | :-------   
`body`          | body of event (decoded as JSON if possible)
`raw_body`      | just the raw event, not decoded
`context`       | just the original context


## Contributing

If you would like to contribute please make sure to follow the established patterns and unit test your code:

### Unit Testing

To run unit test, enter command:
```bash
pipenv run test
```
