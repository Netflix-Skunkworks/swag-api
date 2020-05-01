"""
.. module: swag_api.resources.namespace
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
from swag_api.parsers import namespace_arguments
from swag_api.responses import jsonify


def basic_metrics(func) -> Callable:
    """Common metric tags that are used by the services endpoints"""
    def wrapper(*args, **kwargs) -> Response:
        g.metric_tags = {
            'method': request.method.lower(),
            'service': 'namespace'
        }

        return func(*args, **kwargs)

    return wrapper


@api.route('/<namespace>')
class NameSpace(Resource):

    method_decorators = [basic_metrics]

    @api.expect(namespace_arguments)
    @api.response(200, 'List of all accounts')
    def get(self, namespace):
        """
        Returns all accounts in the namespace.
        Example: For a namespace `accounts`, a list of accounts will be returned based on [Account Schema](https://github.com/Netflix-Skunkworks/swag-client/blob/master/swag_client/schemas/v2.py#L43)
        """
        g.metric_tags.update({'endpoint': 'namespace.list_all'})
        swag.namespace = namespace
        return jsonify(swag.get_all())
