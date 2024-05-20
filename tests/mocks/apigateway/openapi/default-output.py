def get():
    return {
        'openapi': '3.1.0',
        'info': {
            'version': '1.0.0',
            'title': 'Acai Generator',
            'license': {
                'name': 'MIT'
            }
        },
        'tags': [
            {
                'name': 'acai_aws-example'
            }
        ],
        'servers': [],
        'paths': {
            '/acai_aws/example/basic': {
                'get': {
                    'tags': [
                        'acai_aws-example'
                    ],
                    'operationId': 'GetAcaiAwsExampleBasicAcaiGenerated',
                    'deprecated': False,
                    'parameters': [
                        {
                            'in': 'query',
                            'name': 'basic_id',
                            'required': True,
                            'schema': {
                                'type': 'string'
                            }
                        },
                        {
                            'in': 'query',
                            'name': 'first',
                            'required': False,
                            'schema': {
                                'type': 'string'
                            }
                        },
                        {
                            'in': 'query',
                            'name': 'last',
                            'required': False,
                            'schema': {
                                'type': 'string'
                            }
                        }
                    ]
                },
                'post': {
                    'tags': [
                        'acai_aws-example'
                    ],
                    'operationId': 'PostAcaiAwsExampleBasicAcaiGenerated',
                    'deprecated': False,
                    'parameters': [],
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    '$ref': '#/components/schemas/post-acai-aws-example-basic-request-body'
                                }
                            }
                        }
                    }
                }
            },
            '/nested_1/nested_2/{id}': {
                'delete': {
                    'tags': [
                        'acai_aws-example'
                    ],
                    'operationId': 'DeleteNested1Nested2IdAcaiGenerated',
                    'deprecated': False,
                    'parameters': [
                        {
                            'in': 'path',
                            'name': 'id',
                            'required': True,
                            'schema': {
                                'type': 'string'
                            }
                        }
                    ]
                },
                'patch': {
                    'tags': [
                        'acai_aws-example'
                    ],
                    'operationId': 'PatchNested1Nested2IdAcaiGenerated',
                    'deprecated': False,
                    'parameters': [
                        {
                            'in': 'path',
                            'name': 'id',
                            'required': True,
                            'schema': {
                                'type': 'string'
                            }
                        }
                    ],
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    '$ref': '#/components/schemas/patch-nested-1-nested-2-id-request-body'
                                }
                            }
                        }
                    }
                }
            },
            '/acai_aws/example/nested_1/nested_2/resource': {
                'put': {
                    'tags': [
                        'acai_aws-example'
                    ],
                    'operationId': 'PutAcaiAwsExampleNested1Nested2ResourceAcaiGenerated',
                    'deprecated': False,
                    'parameters': []
                }
            },
            '/acai_aws/example/{dynamic}': {
                'get': {
                    'tags': [
                        'acai_aws-example'
                    ],
                    'operationId': 'GetAcaiAwsExampleDynamicAcaiGenerated',
                    'deprecated': False,
                    'security': [
                        {
                            'AcaiGenerated': []
                        }
                    ],
                    'parameters': [
                        {
                            'in': 'header',
                            'name': 'x-dynamic-key',
                            'required': True,
                            'schema': {
                                'type': 'string'
                            }
                        },
                        {
                            'in': 'path',
                            'name': 'dynamic',
                            'required': True,
                            'schema': {
                                'type': 'string'
                            }
                        }
                    ],
                    'responses': {
                        '200': {
                            'description': 'OK',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        '$ref': '#/components/schemas/get-acai-aws-example-dynamic-response-body'
                                    }
                                }
                            }
                        }
                    }
                },
                'post': {
                    'tags': [
                        'acai_aws-example'
                    ],
                    'operationId': 'PostAcaiAwsExampleDynamicAcaiGenerated',
                    'deprecated': False,
                    'security': [
                        {
                            'AcaiGenerated': []
                        }
                    ],
                    'parameters': [
                        {
                            'in': 'path',
                            'name': 'dynamic',
                            'required': True,
                            'schema': {
                                'type': 'string'
                            }
                        }
                    ],
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    '$ref': '#/components/schemas/post-acai-aws-example-dynamic-request-body'
                                }
                            }
                        }
                    }
                }
            }
        },
        'components': {
            'securitySchemes': {
                'AcaiGenerated': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'CHANGE-ME'
                }
            },
            'schemas': {
                'post-acai-aws-example-basic-request-body': {
                    'properties': {
                        'id': {
                            'exclusiveMinimum': 0,
                            'title': 'Id',
                            'type': 'integer'
                        },
                        'email': {
                            'title': 'Email',
                            'type': 'string'
                        },
                        'active': {
                            'title': 'Active',
                            'type': 'boolean'
                        },
                        'favorites': {
                            'items': {
                                'type': 'string'
                            },
                            'title': 'Favorites',
                            'type': 'array'
                        },
                        'notification_config': {
                            'additionalProperties': {
                                'type': 'boolean'
                            },
                            'title': 'Notification Config',
                            'type': 'object'
                        }
                    },
                    'required': [
                        'id',
                        'email',
                        'active',
                        'favorites',
                        'notification_config'
                    ],
                    'title': 'UserRequest',
                    'type': 'object'
                },
                'patch-nested-1-nested-2-id-request-body': {
                    'type': 'object',
                    'required': [],
                    'additionalProperties': False,
                    'properties': {
                        'grower_id': {
                            'type': 'string'
                        },
                        'body': {
                            'type': 'object'
                        },
                        'dict': {
                            'type': 'boolean'
                        }
                    }
                },
                'get-acai-aws-example-dynamic-response-body': {
                    'type': 'object',
                    'required': [
                        'dynamic_id',
                        'dynamic_bool',
                        'dynamic_message'
                    ],
                    'additionalProperties': False,
                    'properties': {
                        'dynamic_id': {
                            'type': 'int'
                        },
                        'dynamic_bool': {
                            'type': 'boolean'
                        },
                        'dynamic_message': {
                            'type': 'string'
                        }
                    }
                },
                'post-acai-aws-example-dynamic-request-body': {
                    'properties': {
                        'id': {
                            'exclusiveMinimum': 0,
                            'title': 'Id',
                            'type': 'integer'
                        },
                        'email': {
                            'title': 'Email',
                            'type': 'string'
                        },
                        'active': {
                            'title': 'Active',
                            'type': 'boolean'
                        },
                        'favorites': {
                            'items': {
                                'type': 'string'
                            },
                            'title': 'Favorites',
                            'type': 'array'
                        },
                        'notification_config': {
                            'additionalProperties': {
                                'type': 'boolean'
                            },
                            'title': 'Notification Config',
                            'type': 'object'
                        }
                    },
                    'required': [
                        'id',
                        'email',
                        'active',
                        'favorites',
                        'notification_config'
                    ],
                    'title': 'UserRequest',
                    'type': 'object'
                }
            }
        }
    }