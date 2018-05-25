from flask import jsonify, request
from flask_restplus import reqparse, Resource
from marshmallow.exceptions import ValidationError

from swag_api.api import api
from swag_api.common.swag import get_account
from swag_api.extensions import swag
from swag_api.parsers import service_simple_arguments, service_account_arguments, service_region_arguments
from swag_api.responses import not_found_response


@api.route('/<namespace>/service/<service>')
class Service(Resource):

    @api.expect(service_simple_arguments)
    @api.response(200, 'List of accounts with service')
    def get(self, namespace, service):
        """
        Returns a list of accounts with the given service.
        """
        swag.namespace = namespace

        accounts = swag.get_service_enabled(service)

        return accounts


@api.route('/<namespace>/service/<account>/<service_name>')
class AccountService(Resource):

    @api.expect(service_account_arguments)
    @api.response(404, 'Service not found in account')
    @api.response(200, 'Service found in account')
    def get(self, namespace, account, service_name):
        """
        Returns the service json for a given account and service name
        """
        swag.namespace = namespace

        account_data = get_account(account)

        if not account_data:
            return not_found_response('account')

        for service in account_data['services']:
            if service['name'] == service_name:
                return service

        return not_found_response('service')

    @api.expect(service_account_arguments)
    @api.response(404, 'Account or Service not found in account')
    @api.response(400, 'Service schema invalid account')
    @api.response(204, 'Service updated in account')
    def post(self, namespace, account, service_name):
        """
        Update service in an account
        Use this method to update the service in an account
        * Send a JSON object with the service schema.
        [Service Schema](https://github.com/Netflix-Skunkworks/swag-client/blob/master/swag_client/schemas/v2.py#L36)
        * Specify the account ID/name and service name in the request URL path.
        """
        json_data = request.get_json(force=True)

        swag.namespace = namespace
        account_data = get_account(account)

        if not account_data:
            return not_found_response('account')

        for service in account_data['services']:
            if service['name'] == service_name:
                account_data["services"].remove(service)
                account_data['services'].append(json_data)
                try:
                    swag.update(account_data)
                except ValidationError as e:
                    return e.messages, 400

                response = jsonify(json_data)
                response.status_code = 204
                return response

        return not_found_response('service')

    @api.expect(service_account_arguments)
    @api.response(404, 'Account not found')
    @api.response(400, 'Service already exists in account')
    @api.response(204, 'Service added in account')
    def put(self, namespace, account, service_name):
        """
        Add service to account
        Use this method to add the service to an account
        * Send a JSON object with the service schema.
        [Service Schema](https://github.com/Netflix-Skunkworks/swag-client/blob/master/swag_client/schemas/v2.py#L36)
        * Specify the account ID/name and service name in the request URL path.
        """
        json_data = request.get_json(force=True)

        swag.namespace = namespace
        account_data = get_account(account)

        if not account_data:
            return not_found_response('account')

        for service in account_data['services']:
            if service['name'] == service_name:
                return { 'service': 'Service already exists' }, 400

        account_data['services'].append(json_data)
        try:
            swag.update(account_data)
        except ValidationError as e:
            return e.messages, 400

        response = jsonify(json_data)
        response.status_code = 204
        return response

    @api.expect(service_account_arguments)
    def delete(self, namespace, account, service_name):
        """
        Delete the service from the given account
        """
        # json_data = request.get_json(force=True)

        swag.namespace = namespace
        account_data = get_account(account)

        if not account_data:
            return not_found_response('account')

        for service in account_data['services']:
            if service['name'] == service_name:
                account_data['services'].remove(service)

                swag.update(account_data)

                return None, 204


@api.route('/<namespace>/service/<account>/<service_name>/toggle')
class ToggleService(Resource):

    @api.expect(service_region_arguments)
    @api.response(204, 'Service status toggled')
    @api.response(404, 'Account or Service not found')
    def post(self, namespace, account, service_name):
        """
        Toggle a service in a given account
        Use this method to toggle the service in an account
        * Send a JSON object with the following json.
        ```
        {
          "enabled": true,  <- required
          "region": "all"   <- optional
        }
        ```
        * Specify the account ID/name and service name in the request URL path.
        """

        args = service_region_arguments.parse_args(request)
        json_data = request.get_json(force=True)
        enabled = json_data['enabled']
        region = json_data.get('region', 'all')

        if not isinstance(enabled, bool):
            return {'enabled': 'Value of enabled must be True or False'}, 400

        swag.namespace = namespace

        account_data = get_account(account)

        if not account_data:
            return not_found_response('account')

        for service in account_data['services']:
            if service['name'] == service_name:
                for status in service['status']:
                    if status['region'] == 'all':
                        status['enabled'] = enabled
                    elif status['region'] == region:
                        status['enabled'] = enabled

                swag.update(account_data)

                return None, 204

        return not_found_response('service')
