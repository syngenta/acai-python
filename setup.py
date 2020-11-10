from setuptools import setup, find_packages

setup(
    name='syngenta_digital_alc',
    version='0.0.1',
    url='https://github.com/syngenta-digital/alc-python.git',
    author='Paul Cruse III, Technical Lead, Syngenta Digital',
    author_email='paul.cruse@syngenta.com',
    description='DRY approach to working with AWS Lambdas',
    long_description=__doc__,
    packages=find_packages(),
    install_requires=[
        'simplejson',
        'jsonschema',
        'jsonref',
        'dynamodb_json'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
