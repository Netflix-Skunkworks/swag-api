"""
.. module: swag_api.api
    :platform: Unix
    :copyright: (c) 2017 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>
"""
from flask import Blueprint, current_app
from flask_restful import reqparse, Api, Resource

from swag_client.backend import SWAGManager
from swag_client.schemas import v2
from swag_client.util import parse_swag_config_options

mod = Blueprint('api', __name__)
api = Api(mod)


class NameSpace(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(NameSpace, self).__init__()

    def get(self, namespace):
        self.reqparse.add_argument('schemaVersion', type=int, default=2)
        args = self.reqparse.parse_args()
        swag_opts = {
            'swag.type': current_app.config.get('SWAG_BACKEND_TYPE', 'dynamodb'),
            'swag.namespace': namespace
        }
        swag = SWAGManager(**parse_swag_config_options(swag_opts))

        if args['schemaVersion'] == 1:
            return {namespace: [v2.downgrade(x) for x in swag.get_all()]}
        return swag.get_all()

api.add_resource(NameSpace, '/<namespace>')
