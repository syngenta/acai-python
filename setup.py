import os
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='acai_aws',
    version=os.getenv('CIRCLE_TAG'),
    url='https://github.com/syngenta/acai-python.git',
    author='Paul Cruse III',
    author_email='paulcruse3@gmail.com',
    description='DRY, configurable, opinionated, minimalist framework for use with AWS Serverless Lambdas',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.0',
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
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ]
)
