from flask import request
from flask_restplus import reqparse, Resource
from marshmallow.exceptions import ValidationError

from swag_api.api import api
from swag_api.extensions import swag
from swag_api.common.swag import get_account
from swag_api.parsers import account_arguments, account_status_arguments, account_id_arguments
from swag_api.responses import not_found_response, jsonify


@api.route('/<namespace>/<account>')
class SingleAccount(Resource):

    @api.expect(account_arguments)
    @api.response(404, 'Account not found')
    @api.response(200, 'Account found')
    def get(self, namespace, account):
        """
        Returns an account given a name or account ID.
        """
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
        swag.namespace = namespace

        json_data = request.get_json(force=True)
        try:
            swag.create(json_data)
        except ValidationError as e:
            return e.messages, 400

        return None, 204


@api.route('/<namespace>/account_status/<account_status>')
class AccountStatus(Resource):

    @api.expect(account_status_arguments)
    @api.response(200, 'Account with account_status found')
    def get(self, namespace, account_status):
        """
        Returns a list of accounts with the given account_status
        """
        swag.namespace = namespace

        account_data = swag.get_all("[?account_status=='{}']".format(account_status))

        if len(account_data) == 0:
            return jsonify([])
        elif len(account_data) == 1:
            return jsonify([account_data])
        else:
            return jsonify(account_data)
