"""
.. module: swag_api.resources.provider
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Will Bengtson <wbengtson@netflix.com>
"""
from flask_restplus import Resource
from swag_api.api import api
from swag_api.extensions import swag
from swag_api.parsers import provider_arguments
from swag_api.responses import jsonify


@api.route('/<namespace>/provider/<provider>')
class Provider(Resource):

    @api.expect(provider_arguments)
    @api.response(404, 'Account with provider not found')
    @api.response(200, 'Account with provider found')
    def get(self, namespace, provider):
        """
        Returns a list of accounts for a given provider.
        """
        swag.namespace = namespace
        account_data = swag.get_all("[?provider=='{}']".format(provider))

        if len(account_data) == 0:
            return jsonify([])
        else:
            return jsonify(account_data)
