"""
.. module: swag_api.resources.environment
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Will Bengtson <wbengtson@netflix.com>
"""
from flask_restplus import Resource
from swag_api.api import api
from swag_api.extensions import swag
from swag_api.parsers import env_arguments
from swag_api.responses import jsonify


@api.route('/<namespace>/env/<env>')
class Environment(Resource):

    @api.expect(env_arguments)
    @api.response(200, 'List of accounts with given environment')
    def get(self, namespace, env):
        """
        Returns a list of accounts for a given environment.
        """
        swag.namespace = namespace
        account_data = swag.get_all("[?environment=='{}']".format(env))

        if len(account_data) == 0:
            return jsonify([])
        else:
            return jsonify(account_data)
