"""
.. module: swag_api.common.health
    :platform: Unix
    :copyright: (c) 2017 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>
"""
from flask import Blueprint

from swag_api.extensions import swag

mod = Blueprint('healthCheck', __name__)


@mod.route('/healthcheck')
def health():
    healthy = swag.health_check()

    if healthy:
        return 'OK', 200
    else:
        return 'BAD', 500
