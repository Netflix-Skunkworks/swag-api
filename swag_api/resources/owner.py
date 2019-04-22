"""
.. module: swag_api.resources.owner
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Will Bengtson <wbengtson@netflix.com>
"""
from flask_restplus import Resource
from swag_api.api import api
from swag_api.extensions import swag
from swag_api.parsers import owner_arguments
from swag_api.responses import jsonify


@api.route('/<namespace>/owner/<owner>')
class Owner(Resource):

    @api.expect(owner_arguments)
    @api.response(404, 'Account with owner not found')
    @api.response(200, 'Account with owner found')
    def get(self, namespace, owner):
        """
        Returns a list of accounts for a given owner.
        """
        swag.namespace = namespace
        account_data = swag.get_all("[?owner=='{}']".format(owner))

        if len(account_data) == 0:
            return jsonify([])
        else:
            return jsonify(account_data)
