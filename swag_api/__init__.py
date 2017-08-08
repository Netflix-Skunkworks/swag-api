from flask.cli import FlaskGroup

from swag_api import factory
from swag_api.api import mod as api_bp

from swag_api.__about__ import (
    __author__, __copyright__, __email__, __license__, __summary__, __title__,
    __uri__, __version__
)


__all__ = [
    "__title__", "__summary__", "__uri__", "__version__", "__author__",
    "__email__", "__license__", "__copyright__",
]


SWAG_API_BLUEPRINTS = (
    api_bp,
)


def create_app(config=None):
    app = factory.create_app(app_name=__name__, blueprints=SWAG_API_BLUEPRINTS, config=None)
    configure_hook(app)
    return app


def configure_hook(app):
    """
    :param app:
    :return:
    """
    from swag_api.decorators import crossdomain
    if app.config.get('CORS'):
        @app.after_request
        @crossdomain(origin=u"http://localhost:3000", methods=['PUT', 'HEAD', 'GET', 'POST', 'OPTIONS', 'DELETE'])
        def after(response):
            return response

cli = FlaskGroup(create_app=create_app)
