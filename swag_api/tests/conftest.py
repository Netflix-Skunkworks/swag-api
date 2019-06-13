"""
.. module: swag_api
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Will Bengtson <wbengtson@netflix.com>
.. moduleauthor:: Mike Grima <mgrima@netflix.com>
"""
import json
import os
from typing import Dict, Tuple

import boto3
import pytest
from flask import Flask
from flask.testing import FlaskClient
from mock import MagicMock
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

    with mock_dynamodb2():
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


@pytest.yield_fixture(scope='function')
def bad_dynamodb_table(aws_credentials):
    with mock_dynamodb2():
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


@pytest.fixture(scope='function')
def swag_app(dynamodb_table) -> Flask:
    from swag_api import create_app

    app = create_app(__name__)
    app.app_context()

    yield app


@pytest.fixture(scope='function')
def swag_app_client(swag_app: Flask) -> FlaskClient:
    yield swag_app.test_client()


@pytest.fixture(scope='function')
def bad_swag_app(bad_dynamodb_table) -> Flask:
    from swag_api import create_app

    yield create_app(__name__)


@pytest.fixture(scope='function')
def swag_app_client_bad(bad_swag_app) -> FlaskClient:
    return bad_swag_app.test_client()


def reset_metrics(swag_app: Flask) -> Tuple[MagicMock, MagicMock]:
    """
    Used to set up the metric mocking for tests that cannot rely on the fixture.

    This can be used if the test function cannot make use of the fixture.
    """
    counter_metric = MagicMock()
    latency_metric = MagicMock()

    swag_app.metrics_plugins['swag_api.plugins.metrics.sample'].send_counter_metric = counter_metric
    swag_app.metrics_plugins['swag_api.plugins.metrics.sample'].send_latency_metric = latency_metric

    return counter_metric, latency_metric


def metrics_tests(counter_metric: MagicMock, latency_metric: MagicMock, expected_tags: Dict[str, str]):
    """
    Used to test the mocked metrics.

    This can be used if the test function cannot make use of the fixture.
    """
    assert counter_metric.called
    assert latency_metric.called

    # Verify that the tags are a Dict[str, str]
    for x, y in expected_tags.items():
        assert isinstance(x, str)
        assert isinstance(y, str)

    assert counter_metric.call_args[0][0] == 'swag_api.request'
    assert counter_metric.call_args[1]['tags'] == expected_tags

    assert latency_metric.call_args[0][0] == 'swag_api.request_latency'
    assert type(latency_metric.call_args[0][1]) is float
    assert latency_metric.call_args[1]['tags'] == expected_tags


@pytest.fixture(scope='function')
def mocked_metrics(swag_app: Flask) -> Dict[str, str]:
    """Mocks out the metrics collectors... And verifies that they are called!"""
    counter_metric, latency_metric = reset_metrics(swag_app)

    # Each test will populate the expected tags and values that should be present.
    # If not present, the test fails.
    expected_tags = {}

    yield expected_tags

    metrics_tests(counter_metric, latency_metric, expected_tags)
