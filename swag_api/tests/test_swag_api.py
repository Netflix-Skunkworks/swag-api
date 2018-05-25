import json
import logging
import time
import unittest

import pytest


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def test_api_1_healthcheck_good_get(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/healthcheck')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'OK'


def test_api_1_healthcheck_bad_get(swag_app_client_bad):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client_bad.get('/api/1/healthcheck')

    assert response.status_code == 500
    assert response.data.decode('utf-8') == 'BAD'


def test_api_1_namespace_get(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/accounts')

    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_api_1_accounts_single_name_get(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/accounts/testaccount')

    assert response.status_code == 200
    assert isinstance(response.get_json(), dict)

def test_api_1_accounts_single_id_get(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/accounts/123456789101')

    assert response.status_code == 200
    assert isinstance(response.get_json(), dict)


def test_api_1_accounts_single_name_not_found_get(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/accounts/anaccountthatdoesnotexist')

    assert response.status_code == 404
    assert response.get_json() == {'account': 'Not found'}


def test_api_1_accounts_single_id_not_found_get(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/accounts/1111111111')

    assert response.status_code == 404
    assert response.get_json() == {'account': 'Not found'}


def test_api_1_accounts_create_valid_schema_put(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

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

    response = swag_app_client.put(
        '/api/1/accounts/012345678910',
        data=json.dumps(account_dict),
        content_type='application/json'
    )

    assert response.status_code == 204

    response = swag_app_client.get('/api/1/accounts')
    assert len(response.get_json()) == 4


def test_api_1_accounts_create_invalid_schema_put(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

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


def test_api_1_accounts_update_valid_schema_put(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

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

    response = swag_app_client.post(
        '/api/1/accounts/012345678910',
        data=json.dumps(account_dict),
        content_type='application/json'
    )
    assert response.status_code == 204

    response = swag_app_client.get('/api/1/accounts/012345678910')
    assert response.get_json()['description'] == 'UPDATED'


def test_api_1_accounts_update_invalid_schema_put(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

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

    response = swag_app_client.post(
        '/api/1/accounts/012345678910',
        data=json.dumps(account_dict),
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.get_json() == {'id': ['Missing data for required field.']}


def test_api_1_service_get(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/accounts/service/myService')

    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_api_1_account_service_get(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/accounts/service/testaccount/myService')

    assert response.status_code == 200
    assert isinstance(response.get_json(), dict)
    assert response.get_json()['name'] == 'myService'


def test_api_1_environment_get(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/accounts/env/test')

    assert response.status_code == 200
    assert len(response.get_json()) == 1

    response = swag_app_client.get('/api/1/accounts/env/prod')

    assert response.status_code == 200
    assert len(response.get_json()) == 2

    response = swag_app_client.get('/api/1/accounts/env/production')

    assert response.status_code == 200
    assert len(response.get_json()) == 0


def test_api_1_owner_get(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/accounts/owner/netflix')

    assert response.status_code == 200
    assert len(response.get_json()) == 1

    response = swag_app_client.get('/api/1/accounts/owner/netflix2')

    assert response.status_code == 200
    assert len(response.get_json()) == 1

    response = swag_app_client.get('/api/1/accounts/owner/fakeowner')

    assert response.status_code == 200
    assert len(response.get_json()) == 0


def test_api_1_provider_get(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/accounts/provider/aws')

    assert response.status_code == 200
    assert len(response.get_json()) == 2

    response = swag_app_client.get('/api/1/accounts/provider/gcp')

    assert response.status_code == 200
    assert len(response.get_json()) == 1

    response = swag_app_client.get('/api/1/accounts/provider/azure')

    assert response.status_code == 200
    assert len(response.get_json()) == 0


def test_api_1_account_status_get(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/accounts/account_status/deleted')

    assert response.status_code == 200
    assert len(response.get_json()) == 1

    response = swag_app_client.get('/api/1/accounts/account_status/ready')

    assert response.status_code == 200
    assert len(response.get_json()) == 2

    response = swag_app_client.get('/api/1/accounts/account_status/created')

    assert response.status_code == 200
    assert len(response.get_json()) == 0


def test_api_1_account_service_toggle_post(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/accounts/service/testaccount/myService')

    assert response.get_json()['status'][0]['enabled']

    toggle_dict = {
        'enabled': False
    }

    response = swag_app_client.post(
        '/api/1/accounts/service/testaccount/myService/toggle',
        data=json.dumps(toggle_dict),
        content_type='application/json'
    )

    assert response.status_code == 204

    response = swag_app_client.get('/api/1/accounts/service/testaccount/myService')

    assert response.get_json()['status'][0]['enabled'] == False


def test_api_1_account_service_delete(swag_app_client):
    from swag_client.backend import SWAGManager
    from swag_client.util import parse_swag_config_options

    response = swag_app_client.get('/api/1/accounts/service/testaccount/myService')

    assert isinstance(response.get_json(), dict)

    response = swag_app_client.delete('/api/1/accounts/service/testaccount/myService')

    assert response.status_code == 204

    response = swag_app_client.get('/api/1/accounts/service/testaccount/myService')

    assert response.status_code == 404
    assert response.get_json() == {'service': 'Not found'}


