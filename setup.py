import os
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='acai_aws',
    version=os.getenv('CIRCLE_TAG', '0.0.0'),
    url='https://github.com/syngenta/acai-python',
    author='Paul Cruse III',
    author_email='paulcruse3@gmail.com',
    description='DRY, configurable, declarative framework for building AWS Lambda APIs and event processors',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'boto3',
        'dynamodb_json',
        'jsonpickle',
        'jsonref',
        'jsonschema',
        'icecream',
        'pydantic',
        'pyyaml',
        'simplejson',
        'xmltodict'
    ],
    keywords=[
        'aws', 'lambda', 'serverless', 'apigateway', 'router', 'openapi', 'pydantic',
        'dynamodb', 'sqs', 'sns', 's3', 'kinesis', 'firehose', 'msk', 'documentdb',
        'event-driven', 'validation', 'jsonschema', 'python-framework'
    ],
    project_urls={
        'Homepage': 'https://github.com/syngenta/acai-python',
        'Documentation': 'https://syngenta.github.io/acai-python-docs/',
        'Source': 'https://github.com/syngenta/acai-python',
        'Issue Tracker': 'https://github.com/syngenta/acai-python/issues',
        'CI/CD': 'https://circleci.com/gh/syngenta/acai-python'
    },
    license='Apache 2.0',
    platforms=['any'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Monitoring',
        'Natural Language :: English'
    ]
)
