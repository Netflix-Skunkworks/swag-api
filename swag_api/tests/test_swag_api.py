"""
.. module: swag_api.extensions
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Will Bengtson <wbengtson@netflix.com>
.. moduleauthor:: Mike Grima <mgrima@netflix.com>
"""
import json
import logging

import pytest
from mock import MagicMock
from swag_api.tests.conftest import metrics_tests, reset_metrics

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def test_api_1_healthcheck_good_get(swag_app_client, mocked_metrics):
    response = swag_app_client.get('/api/1/healthcheck')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'OK'

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'get',
        'service': 'healthcheck',
        'status_code': '200'
    })


def test_api_1_healthcheck_bad_get(bad_swag_app, swag_app_client_bad):
    counter_metric, latency_metric = reset_metrics(bad_swag_app)
    response = swag_app_client_bad.get('/api/1/healthcheck')

    assert response.status_code == 500
    assert response.data.decode('utf-8') == 'BAD'

    mocked_metrics = {
        'method': 'get',
        'service': 'healthcheck',
        'status_code': '500'
    }
    metrics_tests(counter_metric, latency_metric, mocked_metrics)


def test_api_1_namespace_get(swag_app_client, mocked_metrics):
    response = swag_app_client.get('/api/1/accounts')

    assert response.status_code == 200
    assert len(response.get_json()) == 3

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'get',
        'service': 'namespace',
        'endpoint': 'namespace.list_all',
        'status_code': '200'
    })


def test_api_1_accounts_single_name_get(swag_app_client, mocked_metrics):
    response = swag_app_client.get('/api/1/accounts/testaccount')

    assert response.status_code == 200
    assert isinstance(response.get_json(), dict)

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'get',
        'service': 'accounts',
        'endpoint': 'accounts.get_single_account',
        'status_code': '200'
    })


def test_api_1_accounts_single_id_get(swag_app_client, mocked_metrics):
    response = swag_app_client.get('/api/1/accounts/123456789101')

    assert response.status_code == 200
    assert isinstance(response.get_json(), dict)

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'get',
        'service': 'accounts',
        'endpoint': 'accounts.get_single_account',
        'status_code': '200'
    })


def test_api_1_accounts_single_name_not_found_get(swag_app_client, mocked_metrics):
    response = swag_app_client.get('/api/1/accounts/anaccountthatdoesnotexist')

    assert response.status_code == 404
    assert response.get_json() == {'account': 'Not found'}

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'get',
        'service': 'accounts',
        'endpoint': 'accounts.get_single_account',
        'status_code': '404'
    })


def test_api_1_accounts_single_id_not_found_get(swag_app_client, mocked_metrics):
    response = swag_app_client.get('/api/1/accounts/1111111111')

    assert response.status_code == 404
    assert response.get_json() == {'account': 'Not found'}

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'get',
        'service': 'accounts',
        'endpoint': 'accounts.get_single_account',
        'status_code': '404'
    })


def test_api_1_accounts_create_valid_schema_put(swag_app, swag_app_client):
    account_dict = {
        'aliases': ['test'],
        'contacts': ['admins@test.net'],
        'description': 'LOL, Test account',
        'email': 'testaccount@test.net',
        'environment': 'test',
        'id': '012345678910',
        'name': 'testaccount',
        'owner': 'netflix',
        'provider': 'aws',
        'sensitive': False
    }
    response = swag_app_client.get('/api/1/accounts')
    assert len(response.get_json()) == 3

    counter_metric, latency_metric = reset_metrics(swag_app)
    response = swag_app_client.put(
        '/api/1/accounts/012345678910',
        data=json.dumps(account_dict),
        content_type='application/json'
    )
    assert response.status_code == 204
    mocked_metrics = {
        'method': 'put',
        'service': 'accounts',
        'endpoint': 'accounts.add_new_account',
        'status_code': '204'
    }
    metrics_tests(counter_metric, latency_metric, mocked_metrics)

    response = swag_app_client.get('/api/1/accounts')
    assert len(response.get_json()) == 4


def test_api_1_accounts_create_invalid_schema_put(swag_app_client, mocked_metrics):
    account_dict = {
        'aliases': ['test'],
        'contacts': ['admins@test.net'],
        'description': 'LOL, Test account',
        'email': 'testaccount@test.net',
        'environment': 'test',
        'name': 'testaccount',
        'owner': 'netflix',
        'provider': 'aws',
        'sensitive': False
    }

    response = swag_app_client.put(
        '/api/1/accounts/012345678910',
        data=json.dumps(account_dict),
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.get_json() == {'id': ['Missing data for required field.']}

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'put',
        'service': 'accounts',
        'endpoint': 'accounts.add_new_account',
        'status_code': '400'
    })


def test_api_1_accounts_update_valid_schema_post(swag_app, swag_app_client):
    account_dict = {
        'aliases': ['test'],
        'contacts': ['admins@test.net'],
        'description': 'LOL, Test account',
        'email': 'testaccount@test.net',
        'environment': 'test',
        'id': '012345678910',
        'name': 'testaccount',
        'owner': 'netflix',
        'provider': 'aws',
        'sensitive': False
    }
    response = swag_app_client.put(
        '/api/1/accounts/012345678910',
        data=json.dumps(account_dict),
        content_type='application/json'
    )
    assert response.status_code == 204

    account_dict['description'] = 'UPDATED'
    counter_metric, latency_metric = reset_metrics(swag_app)
    response = swag_app_client.post(
        '/api/1/accounts/012345678910',
        data=json.dumps(account_dict),
        content_type='application/json'
    )
    assert response.status_code == 204

    mocked_metrics = {
        'method': 'post',
        'service': 'accounts',
        'endpoint': 'accounts.update_account',
        'status_code': '204'
    }
    metrics_tests(counter_metric, latency_metric, mocked_metrics)

    response = swag_app_client.get('/api/1/accounts/012345678910')
    assert response.get_json()['description'] == 'UPDATED'


def test_api_1_accounts_update_invalid_schema_put(swag_app, swag_app_client):
    account_dict = {
        'aliases': ['test'],
        'contacts': ['admins@test.net'],
        'description': 'LOL, Test account',
        'email': 'testaccount@test.net',
        'environment': 'test',
        'id': '012345678910',
        'name': 'testaccount',
        'owner': 'netflix',
        'provider': 'aws',
        'sensitive': False
    }
    response = swag_app_client.put(
        '/api/1/accounts/012345678910',
        data=json.dumps(account_dict),
        content_type='application/json'
    )
    assert response.status_code == 204

    del account_dict['id']
    counter_metric, latency_metric = reset_metrics(swag_app)
    response = swag_app_client.post(
        '/api/1/accounts/012345678910',
        data=json.dumps(account_dict),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.get_json() == {'id': ['Missing data for required field.']}

    mocked_metrics = {
        'method': 'post',
        'service': 'accounts',
        'endpoint': 'accounts.update_account',
        'status_code': '400'
    }
    metrics_tests(counter_metric, latency_metric, mocked_metrics)


def test_api_1_service_get(swag_app_client, mocked_metrics):
    """Tests /<namespace>/service/<service>"""
    response = swag_app_client.get('/api/1/accounts/service/myService')

    assert response.status_code == 200
    assert len(response.get_json()) == 1

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'get',
        'service': 'service',
        'endpoint': 'service.all_accounts_with_service',
        'status_code': '200'
    })


def test_api_1_account_service_get(swag_app_client, mocked_metrics):
    """Tests GET on /<namespace>/service/<account>/<service_name>"""
    response = swag_app_client.get('/api/1/accounts/service/testaccount/myService')

    assert response.status_code == 200
    assert isinstance(response.get_json(), dict)
    assert response.get_json()['name'] == 'myService'

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'get',
        'service': 'service',
        'endpoint': 'service.get_service_for_account',
        'status_code': '200'
    })


def test_api_1_account_service_no_account_found_get(swag_app_client, mocked_metrics):
    """Tests GET 404 on /<namespace>/service/<account>/<service_name>"""
    response = swag_app_client.get('/api/1/accounts/service/idonotexist/myService')

    assert response.status_code == 404
    assert response.get_json() == {'account': 'Not found'}

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'get',
        'service': 'service',
        'endpoint': 'service.get_service_for_account',
        'status_code': '404'
    })


@pytest.mark.parametrize("env,length", [('test', 1), ('prod', 2), ('production', 0)])
def test_api_1_environment_get(swag_app_client, env, length, mocked_metrics):
    response = swag_app_client.get(f'/api/1/accounts/env/{env}')
    assert response.status_code == 200
    assert len(response.get_json()) == length

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'get',
        'service': 'environment',
        'endpoint': 'environment.list_accounts_in_environment',
        'status_code': '200'
    })


@pytest.mark.parametrize("owner,length", [('netflix', 1), ('netflix2', 1), ('fakeowner', 0)])
def test_api_1_owner_get(swag_app_client, owner, length, mocked_metrics):
    response = swag_app_client.get(f'/api/1/accounts/owner/{owner}')

    assert response.status_code == 200
    assert len(response.get_json()) == length

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'get',
        'service': 'owner',
        'endpoint': 'owner.list_accounts_with_owner',
        'status_code': '200'
    })


@pytest.mark.parametrize("provider,length", [('aws', 2), ('gcp', 1), ('azure', 0)])
def test_api_1_provider_get(swag_app_client, provider, length, mocked_metrics):
    response = swag_app_client.get(f'/api/1/accounts/provider/{provider}')

    assert response.status_code == 200
    assert len(response.get_json()) == length

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'get',
        'service': 'provider',
        'endpoint': 'provider.list_accounts_on_provider',
        'status_code': '200'
    })


@pytest.mark.parametrize("status,length", [('deleted', 1), ('ready', 2), ('created', 0)])
def test_api_1_account_status_get(swag_app_client, status, length, mocked_metrics):
    response = swag_app_client.get(f'/api/1/accounts/account_status/{status}')

    assert response.status_code == 200
    assert len(response.get_json()) == length

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'get',
        'service': 'accounts',
        'endpoint': 'accounts.get_accounts_with_status',
        'status_code': '200'
    })


def test_api_1_account_service_toggle_post(swag_app, swag_app_client):
    response = swag_app_client.get('/api/1/accounts/service/testaccount/myService')
    assert response.get_json()['status'][0]['enabled']
    toggle_dict = {
        'enabled': False
    }

    counter_metric, latency_metric = reset_metrics(swag_app)
    response = swag_app_client.post(
        '/api/1/accounts/service/testaccount/myService/toggle',
        data=json.dumps(toggle_dict),
        content_type='application/json'
    )
    assert response.status_code == 204
    mocked_metrics = {
        'method': 'post',
        'service': 'service',
        'endpoint': 'service.toggle_service_for_account',
        'status_code': '204'
    }
    metrics_tests(counter_metric, latency_metric, mocked_metrics)

    response = swag_app_client.get('/api/1/accounts/service/testaccount/myService')
    assert not response.get_json()['status'][0]['enabled']


def test_api_1_account_service_toggle_region_post(swag_app_client, mocked_metrics):
    toggle_dict = {
        'enabled': False,
        'region': 'us-east-1'
    }

    response = swag_app_client.post(
        '/api/1/accounts/service/testaccount/myService2/toggle',
        data=json.dumps(toggle_dict),
        content_type='application/json'
    )
    assert response.status_code == 204

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'post',
        'service': 'service',
        'endpoint': 'service.toggle_service_for_account',
        'status_code': '204'
    })


def test_api_1_account_service_toggle_invalid_json_post(swag_app_client, mocked_metrics):
    toggle_dict = {
        'enabled': 'False'
    }

    response = swag_app_client.post(
        '/api/1/accounts/service/testaccount/myService/toggle',
        data=json.dumps(toggle_dict),
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.get_json() == {'enabled': 'Value of enabled must be True or False'}

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'post',
        'service': 'service',
        'endpoint': 'service.toggle_service_for_account',
        'status_code': '400'
    })


def test_api_1_account_service_toggle_service_not_found_post(swag_app_client, mocked_metrics):
    toggle_dict = {
        'enabled': False
    }

    response = swag_app_client.post(
        '/api/1/accounts/service/testaccount/myFakeService/toggle',
        data=json.dumps(toggle_dict),
        content_type='application/json'
    )

    assert response.status_code == 404
    assert response.get_json() == {'service': 'Not found'}

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'post',
        'service': 'service',
        'endpoint': 'service.toggle_service_for_account',
        'status_code': '404'
    })


def test_api_1_account_service_toggle_account_not_found_post(swag_app_client, mocked_metrics):
    toggle_dict = {
        'enabled': False
    }

    response = swag_app_client.post(
        '/api/1/accounts/service/idonotexist/myService/toggle',
        data=json.dumps(toggle_dict),
        content_type='application/json'
    )

    assert response.status_code == 404
    assert response.get_json() == {'account': 'Not found'}

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'post',
        'service': 'service',
        'endpoint': 'service.toggle_service_for_account',
        'status_code': '404'
    })


def test_api_1_account_service_delete(swag_app, swag_app_client):
    response = swag_app_client.get('/api/1/accounts/service/testaccount/myService')
    assert isinstance(response.get_json(), dict)

    counter_metric, latency_metric = reset_metrics(swag_app)
    response = swag_app_client.delete('/api/1/accounts/service/testaccount/myService')
    assert response.status_code == 204

    mocked_metrics = {
        'method': 'delete',
        'service': 'service',
        'endpoint': 'service.delete_service_from_account',
        'status_code': '204'
    }
    metrics_tests(counter_metric, latency_metric, mocked_metrics)

    response = swag_app_client.get('/api/1/accounts/service/testaccount/myService')
    assert response.status_code == 404
    assert response.get_json() == {'service': 'Not found'}


def test_api_1_account_service_account_not_found_delete(swag_app_client, mocked_metrics):
    response = swag_app_client.delete('/api/1/accounts/service/idonotexist/myService')

    assert response.status_code == 404
    assert response.get_json() == {'account': 'Not found'}

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'delete',
        'service': 'service',
        'endpoint': 'service.delete_service_from_account',
        'status_code': '404'
    })


def test_api_1_account_service_add_valid_schema_put(swag_app, swag_app_client):
    response = swag_app_client.get('/api/1/accounts/service/testaccount/myNewService')
    assert response.status_code == 404

    netflix_service = {
        'name': 'myNewService',
        'status': [{
            'region': 'all',
            'enabled': True,
            'notes': []
        }],
        'metadata': {
        },
        'roles': []
    }
    counter_metric, latency_metric = reset_metrics(swag_app)
    response = swag_app_client.put(
        '/api/1/accounts/service/testaccount/myNewService',
        data=json.dumps(netflix_service),
        content_type='application/json'
    )
    assert response.status_code == 204

    mocked_metrics = {
        'method': 'put',
        'service': 'service',
        'endpoint': 'service.add_service_for_account',
        'status_code': '204'
    }
    metrics_tests(counter_metric, latency_metric, mocked_metrics)

    response = swag_app_client.get('/api/1/accounts/service/testaccount/myNewService')
    assert response.status_code == 200
    assert response.get_json()['name'] == 'myNewService'


def test_api_1_account_service_add_invalid_schema_put(swag_app, swag_app_client):
    response = swag_app_client.get('/api/1/accounts/service/testaccount/myNewService')
    assert response.status_code == 404

    netflix_service = {
        'status': [{
            'region': 'all',
            'enabled': True,
            'notes': []
        }],
        'metadata': {
        },
        'roles': []
    }
    counter_metric, latency_metric = reset_metrics(swag_app)
    response = swag_app_client.put(
        '/api/1/accounts/service/testaccount/myNewService',
        data=json.dumps(netflix_service),
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.get_json() == {'services': {'3': {'name': ['Missing data for required field.']}}}

    mocked_metrics = {
        'method': 'put',
        'service': 'service',
        'endpoint': 'service.add_service_for_account',
        'status_code': '400'
    }
    metrics_tests(counter_metric, latency_metric, mocked_metrics)


def test_api_1_account_service_add_valid_schema_invalid_account_put(swag_app_client, mocked_metrics):
    netflix_service = {
        'name': 'myNewService',
        'status': [{
            'region': 'all',
            'enabled': True,
            'notes': []
        }],
        'metadata': {
        },
        'roles': []
    }
    response = swag_app_client.put(
        '/api/1/accounts/service/idonotexist/myNewService',
        data=json.dumps(netflix_service),
        content_type='application/json'
    )

    assert response.status_code == 404
    assert response.get_json() == {'account': 'Not found'}

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'put',
        'service': 'service',
        'endpoint': 'service.add_service_for_account',
        'status_code': '404'
    })


def test_api_1_account_service_add_service_exists_put(swag_app_client, mocked_metrics):
    netflix_service = {
        'name': 'myService',
        'status': [{
            'region': 'all',
            'enabled': True,
            'notes': []
        }],
        'metadata': {
        },
        'roles': []
    }
    response = swag_app_client.put(
        '/api/1/accounts/service/testaccount/myService',
        data=json.dumps(netflix_service),
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.get_json() == {'service': 'Service already exists'}

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'put',
        'service': 'service',
        'endpoint': 'service.add_service_for_account',
        'status_code': '400'
    })


def test_api_1_account_service_updated_valid_schema_post(swag_app, swag_app_client):
    response = swag_app_client.get('/api/1/accounts/service/testaccount/myService')
    assert response.status_code == 200

    netflix_service = {
        'name': 'myService',
        'status': [{
            'region': 'all',
            'enabled': True,
            'notes': []
        }],
        'metadata': {
            'updated': 'yesterday'
        },
        'roles': []
    }
    counter_metric, latency_metric = reset_metrics(swag_app)
    response = swag_app_client.post(
        '/api/1/accounts/service/testaccount/myService',
        data=json.dumps(netflix_service),
        content_type='application/json'
    )
    assert response.status_code == 204

    mocked_metrics = {
        'method': 'post',
        'service': 'service',
        'endpoint': 'service.update_service_for_account',
        'status_code': '204'
    }
    metrics_tests(counter_metric, latency_metric, mocked_metrics)

    response = swag_app_client.get('/api/1/accounts/service/testaccount/myService')
    assert response.status_code == 200
    assert response.get_json()['metadata']['updated'] == 'yesterday'


def test_api_1_account_service_updated_invalid_schema_post(swag_app, swag_app_client):
    response = swag_app_client.get('/api/1/accounts/service/testaccount/myService')
    assert response.status_code == 200

    netflix_service = {
        'status': [{
            'region': 'all',
            'enabled': True,
            'notes': []
        }],
        'metadata': {
            'updated': 'yesterday'
        },
        'roles': []
    }
    counter_metric, latency_metric = reset_metrics(swag_app)
    response = swag_app_client.post(
        '/api/1/accounts/service/testaccount/myService',
        data=json.dumps(netflix_service),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.get_json() == {'services': {'2': {'name': ['Missing data for required field.']}}}

    mocked_metrics = {
        'method': 'post',
        'service': 'service',
        'endpoint': 'service.update_service_for_account',
        'status_code': '400'
    }
    metrics_tests(counter_metric, latency_metric, mocked_metrics)


def test_api_1_account_service_updated_valid_schema_invalid_account_post(swag_app_client, mocked_metrics):
    netflix_service = {
        'name': 'myNewService',
        'status': [{
            'region': 'all',
            'enabled': True,
            'notes': []
        }],
        'metadata': {
        },
        'roles': []
    }
    response = swag_app_client.post(
        '/api/1/accounts/service/idonotexist/myService',
        data=json.dumps(netflix_service),
        content_type='application/json'
    )

    assert response.status_code == 404
    assert response.get_json() == {'account': 'Not found'}

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'post',
        'service': 'service',
        'endpoint': 'service.update_service_for_account',
        'status_code': '404'
    })


def test_api_1_account_service_updated_service_not_found_post(swag_app_client, mocked_metrics):
    netflix_service = {
        'name': 'notRealService',
        'status': [{
            'region': 'all',
            'enabled': True,
            'notes': []
        }],
        'metadata': {
            'updated': 'yesterday'
        },
        'roles': []
    }
    response = swag_app_client.post(
        '/api/1/accounts/service/testaccount/notRealService',
        data=json.dumps(netflix_service),
        content_type='application/json'
    )

    assert response.status_code == 404
    assert response.get_json() == {'service': 'Not found'}

    # Verify the metric tags are passed in correctly -- verified in the mocked_metrics fixture
    mocked_metrics.update({
        'method': 'post',
        'service': 'service',
        'endpoint': 'service.update_service_for_account',
        'status_code': '404'
    })


def test_metrics_plugin_loading(swag_app):
    from swag_api.plugins.metrics import MetricsPlugin
    from swag_api.plugins.metrics.sample.module import SamplePlugin
    assert isinstance(swag_app.metrics_plugins['swag_api.plugins.metrics.sample'], MetricsPlugin)
    assert isinstance(swag_app.metrics_plugins['swag_api.plugins.metrics.sample'], SamplePlugin)

    swag_app.logger = MagicMock()
    swag_app.metrics_plugins['swag_api.plugins.metrics.sample'].send_counter_metric('testing', tags={'some': 'value'})

    assert swag_app.logger.info.called
    assert swag_app.logger.info.call_args_list[0][0][0] == 'Metrics collected for counter: testing, tags: {\'some\': \'value\'}'
