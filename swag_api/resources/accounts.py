"""
.. module: swag_api.resources.accounts
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Will Bengtson <wbengtson@netflix.com>
.. moduleauthor:: Mike Grima <mgrima@netflix.com>
"""
from typing import Callable

from flask import g, request, Response
from flask_restx import Resource
from marshmallow.exceptions import ValidationError
from swag_api.api import api
from swag_api.extensions import swag
from swag_api.common.swag import get_account
from swag_api.parsers import account_arguments, account_id_arguments, account_status_arguments
from swag_api.responses import jsonify, not_found_response


def basic_metrics(func) -> Callable:
    """Common metric tags that are used by the services endpoints"""
    def wrapper(*args, **kwargs) -> Response:
        g.metric_tags = {
            'method': request.method.lower(),
            'service': 'accounts'
        }

        return func(*args, **kwargs)

    return wrapper


@api.route('/<namespace>/<account>')
class SingleAccount(Resource):

    method_decorators = [basic_metrics]

    @api.expect(account_arguments)
    @api.response(404, 'Account not found')
    @api.response(200, 'Account found')
    def get(self, namespace, account):
        """
        Returns an account given a name or account ID.
        """
        g.metric_tags.update({'endpoint': 'accounts.get_single_account'})
        swag.namespace = namespace
        account_data = get_account(account)

        if not account_data:
            return not_found_response('account')
        else:
            return jsonify(account_data)

    @api.expect(account_arguments)
    @api.response(204, 'Account successfully updated.')
    @api.response(400, 'Invalid Account Schema')
    def post(self, namespace, account):
        """
        Update an account
        Use this method to update an account in the namespace
        * Send a JSON object with the new account structure .
        [Account Schema](https://github.com/Netflix-Skunkworks/swag-client/blob/master/swag_client/schemas/v2.py#L43)
        * Specify the ID or name of the account in the request URL path.
        """
        g.metric_tags.update({'endpoint': 'accounts.update_account'})
        swag.namespace = namespace
        json_data = request.get_json(force=True)

        try:
            swag.update(json_data)
        except ValidationError as e:
            return e.messages, 400

        return None, 204

    @api.expect(account_id_arguments)
    @api.response(204, 'Account successfully added.')
    @api.response(400, 'Invalid Account Schema')
    def put(self, namespace, account):
        """
        Add a new account
        Use this method to add a new account to the namespace
        * Send a JSON object with the new account structure .
        [Account Schema](https://github.com/Netflix-Skunkworks/swag-client/blob/master/swag_client/schemas/v2.py#L43)
        * Specify the ID of the account in the request URL path.
        """
        g.metric_tags.update({'endpoint': 'accounts.add_new_account'})
        swag.namespace = namespace
        json_data = request.get_json(force=True)

        try:
            swag.create(json_data)
        except ValidationError as e:
            return e.messages, 400

        return None, 204


@api.route('/<namespace>/account_status/<account_status>')
class AccountStatus(Resource):

    method_decorators = [basic_metrics]

    @api.expect(account_status_arguments)
    @api.response(200, 'Accounts with the account_status')
    def get(self, namespace, account_status):
        """
        Returns a list of accounts with the given account_status
        """
        g.metric_tags.update({'endpoint': 'accounts.get_accounts_with_status'})
        swag.namespace = namespace
        account_data = swag.get_all("[?account_status=='{}']".format(account_status))

        if len(account_data) == 0:
            return jsonify([])
        elif len(account_data) == 1:
            return jsonify([account_data])
        else:
            return jsonify(account_data)
