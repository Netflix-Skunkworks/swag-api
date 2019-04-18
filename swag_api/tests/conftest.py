"""
.. module: swag_api
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Will Bengtson <wbengtson@netflix.com>
"""
import json
import os

import boto3
import pytest
from moto import mock_dynamodb2


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.yield_fixture(scope='function')
def dynamodb_table(aws_credentials):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options
    mock_dynamodb2().start()
    resource = boto3.resource('dynamodb', region_name='us-east-1')

    table = resource.create_table(
        TableName='accounts',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        })

    table.meta.client.get_waiter('table_exists').wait(TableName='accounts')

    swag_opts = {
        'swag.type': 'dynamodb',
        'swag.namespace': 'accounts',
        'swag.cache_expires': 0
    }
    swag = SWAGManager(**parse_swag_config_options(swag_opts))

    cwd = os.path.dirname(os.path.realpath(__file__))
    account_file = os.path.join(cwd, 'vectors/accounts.json')

    with open(account_file, 'r') as f:
        accounts = json.loads(f.read())

        for account in accounts:
            swag.create(account)
    yield
    mock_dynamodb2().stop()


@pytest.yield_fixture(scope='function')
def bad_dynamodb_table(aws_credentials):
    mock_dynamodb2().start()
    resource = boto3.resource('dynamodb', region_name='us-east-1')

    table = resource.create_table(
        TableName='badaccounts',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        })

    table.meta.client.get_waiter('table_exists').wait(TableName='badaccounts')

    yield
    mock_dynamodb2().stop()


@pytest.fixture(scope='function')
def swag_app_client(dynamodb_table):
    from swag_api import create_app

    app = create_app(__name__)

    return app.test_client()


@pytest.fixture(scope='function')
def swag_app_client_bad(bad_dynamodb_table):
    from swag_api import create_app

    app = create_app(__name__)

    return app.test_client()
