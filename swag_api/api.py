"""
.. module: swag_api.api
    :platform: Unix
    :copyright: (c) 2017 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>
"""
from flask import Blueprint, current_app, Request
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
        swag_opts = {
            'swag.type': current_app.config.get('SWAG_BACKEND_TYPE', 'dynamodb'),
            'swag.namespace': namespace
        }
        swag = SWAGManager(**parse_swag_config_options(swag_opts))

        return swag.get_all()

    def post(self, namespace, item):
        swag_opts = {
            'swag.type': current_app.config.get('SWAG_BACKEND_TYPE', 'dynamodb'),
            'swag.namespace': namespace
        }
        swag = SWAGManager(**parse_swag_config_options(swag_opts))
        swag.update(item)


api.add_resource(NameSpace, '/<namespace>')
