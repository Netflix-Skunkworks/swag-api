"""
.. module: swag_api.resources.namespace
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Will Bengtson <wbengtson@netflix.com>
"""
from flask_restplus import Resource
from swag_api.api import api
from swag_api.extensions import swag
from swag_api.parsers import namespace_arguments
from swag_api.responses import jsonify


@api.route('/<namespace>')
class NameSpace(Resource):

    @api.expect(namespace_arguments)
    @api.response(200, 'List of all accounts')
    def get(self, namespace):
        """
        Returns all accounts in the namespace.
        Example: For a namespace `accounts`, a list of accounts will be returned based on [Account Schema](https://github.com/Netflix-Skunkworks/swag-client/blob/master/swag_client/schemas/v2.py#L43)
        """
        swag.namespace = namespace
        return jsonify(swag.get_all())
