"""
.. module: swag_api.api
    :platform: Unix
    :copyright: (c) 2017 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>
"""
from flask import Blueprint
from flask_restx import Api

mod = Blueprint('api', __name__)
api = Api(mod,
          doc='/swagger/', title='SWAG',
          description='A cloud account management system',
          default='/api/1',
          default_label='Operations on Accounts',
          catch_all_404s=True)
