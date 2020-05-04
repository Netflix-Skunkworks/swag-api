"""
.. module: swag_api.resources.owner
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Will Bengtson <wbengtson@netflix.com>
.. moduleauthor:: Mike Grima <mgrima@netflix.com>
"""
from typing import Callable

from flask import g, request, Response
from flask_restx import Resource
from swag_api.api import api
from swag_api.extensions import swag
from swag_api.parsers import owner_arguments
from swag_api.responses import jsonify


def basic_metrics(func) -> Callable:
    """Common metric tags that are used by the services endpoints"""
    def wrapper(*args, **kwargs) -> Response:
        g.metric_tags = {
            'method': request.method.lower(),
            'service': 'owner'
        }

        return func(*args, **kwargs)

    return wrapper


@api.route('/<namespace>/owner/<owner>')
class Owner(Resource):

    method_decorators = [basic_metrics]

    @api.expect(owner_arguments)
    @api.response(200, 'Accounts with the owner')
    def get(self, namespace, owner):
        """
        Returns a list of accounts for a given owner.
        """
        g.metric_tags.update({'endpoint': 'owner.list_accounts_with_owner'})
        swag.namespace = namespace
        account_data = swag.get_all("[?owner=='{}']".format(owner))

        if len(account_data) == 0:
            return jsonify([])
        else:
            return jsonify(account_data)
