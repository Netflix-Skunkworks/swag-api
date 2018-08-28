"""
.. module: swag_api.factory
    :platform: Unix
    :synopsis: This module contains all the needed functions to allow
    the factory app creation.
    :copyright: (c) 2017 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>
"""
import os
import types
import errno

from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_cors import CORS

from swag_api.common.health import mod as health
from swag_api.extensions import sentry, swag
from swag_client.util import parse_swag_config_options

DEFAULT_BLUEPRINTS = (
    health,
)


API_VERSION = 1


def create_app(app_name=None, blueprints=None, config=None):
    """
    swag_api application factory
    :param config:
    :param app_name:
    :param blueprints:
    :return:
    """
    if not blueprints:
        blueprints = DEFAULT_BLUEPRINTS
    else:
        blueprints = blueprints + DEFAULT_BLUEPRINTS

    if not app_name:
        app_name = __name__

    app = Flask(app_name)
    configure_app(app, config)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_logging(app)

    if app.config.get('CORS_ENABLED'):
        cors_resources = app.config.get('CORS_RESOURCES')
        if cors_resources:
            CORS(app, resources=cors_resources)
        else:
            CORS(app)
    return app


def from_file(file_path, silent=False):
    """
    Updates the values in the config from a Python file.  This function
    behaves as if the file was imported as module with the
    :param file_path:
    :param silent:
    """
    d = types.ModuleType('config')
    d.__file__ = file_path
    try:
        with open(file_path) as config_file:
            exec(compile(config_file.read(),  # nosec: config file safe
                 file_path, 'exec'), d.__dict__)
    except IOError as e:
        if silent and e.errno in (errno.ENOENT, errno.EISDIR):
            return False
        e.strerror = 'Unable to load configuration file (%s)' % e.strerror
        raise
    return d


def configure_app(app, config=None):
    """
    Different ways of configuration
    :param app:
    :param config:
    :return:
    """
    # respect the config first
    if config and config != 'None':
        app.config['CONFIG_PATH'] = config
        app.config.from_object(from_file(config))
    else:
        try:
            app.config.from_envvar("SWAG_API_CONF")
        except RuntimeError:
            # look in default paths
            if os.path.isfile(os.path.expanduser("~/.swag/swag_api.conf.py")):
                app.config.from_object(from_file(os.path.expanduser("~/.swag/swag_api.conf.py")))
            else:
                app.config.from_object(from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'default.conf.py')))


def configure_extensions(app):
    """
    Attaches and configures any needed flask extensions
    to our app.
    :param app:
    """
    sentry.init_app(app)

    opts = {
        'swag.type': app.config.get('SWAG_BACKEND_TYPE', 'dynamodb'),
        'swag.namespace': app.config.get('SWAG_BACKEND_NAMESPACE', 'accounts'),
        'swag.schema_context': app.config.get('SWAG_SCHEMA_CONTEXT', {})
    }

    swag.configure(**parse_swag_config_options(opts))


def configure_blueprints(app, blueprints):
    """
    We prefix our APIs with their given version so that we can support
    multiple concurrent API versions.
    :param app:
    :param blueprints:
    """
    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix="/api/{0}".format(API_VERSION))


def configure_logging(app):
    """
    Sets up application wide logging.
    :param app:
    """
    from flask.logging import default_handler
    app.logger.removeHandler(default_handler)

    handler = RotatingFileHandler(app.config.get('LOG_FILE', 'swag_client.log'), maxBytes=10000000, backupCount=100)

    handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))

    handler.setLevel(app.config.get('LOG_LEVEL', 'DEBUG'))
    app.logger.setLevel(app.config.get('LOG_LEVEL', 'DEBUG'))
    app.logger.addHandler(handler)

    if os.environ.get('ENABLE_STREAM_LOGGING', False):
        stream_handler = StreamHandler()
        stream_handler.setLevel(app.config.get('LOG_LEVEL', 'DEBUG'))
        app.logger.addHandler(stream_handler)
