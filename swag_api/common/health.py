"""
.. module: swag_api.common.health
    :platform: Unix
    :copyright: (c) 2017 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>
"""
from flask import Blueprint

mod = Blueprint('healthCheck', __name__)


@mod.route('/healthcheck')
def health():
    return 'ok'


# TODO create dynamobased healthcheck
def healthcheck(db):
    with db.engine.connect() as connection:
        connection.execute('SELECT 1;')
    return True
