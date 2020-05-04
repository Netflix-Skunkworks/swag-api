"""
.. module: swag_api.resources.provider
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
from swag_api.parsers import provider_arguments
from swag_api.responses import jsonify


def basic_metrics(func) -> Callable:
    """Common metric tags that are used by the services endpoints"""
    def wrapper(*args, **kwargs) -> Response:
        g.metric_tags = {
            'method': request.method.lower(),
            'service': 'provider'
        }

        return func(*args, **kwargs)

    return wrapper


@api.route('/<namespace>/provider/<provider>')
class Provider(Resource):

    method_decorators = [basic_metrics]

    @api.expect(provider_arguments)
    @api.response(200, 'Accounts with the provider')
    def get(self, namespace, provider):
        """
        Returns a list of accounts for a given provider.
        """
        g.metric_tags.update({'endpoint': 'provider.list_accounts_on_provider'})
        swag.namespace = namespace
        account_data = swag.get_all("[?provider=='{}']".format(provider))

        if len(account_data) == 0:
            return jsonify([])
        else:
            return jsonify(account_data)
