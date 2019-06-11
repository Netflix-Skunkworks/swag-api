"""
.. module: swag_api.common.health
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>
.. moduleauthor:: Mike Grima <mgrima@netflix.com>
"""
from flask import Blueprint, g, request
from swag_api.extensions import swag

mod = Blueprint('healthCheck', __name__)


@mod.route('/healthcheck')
def health():
    g.metric_tags = {
        'method': request.method.lower(),
        'service': 'healthcheck'
    }

    healthy = swag.health_check()

    if healthy:
        return 'OK', 200
    else:
        return 'BAD', 500
