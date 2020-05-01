"""
.. module: swag_api
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Will Bengtson <wbengtson@netflix.com>
"""
from flask import Flask
from flask.cli import FlaskGroup
from swag_api import factory
from swag_api.api import mod as api_bp
import swag_api.resources.accounts      # noqa: F401
import swag_api.resources.environment   # noqa: F401
import swag_api.resources.namespace     # noqa: F401
import swag_api.resources.owner         # noqa: F401
import swag_api.resources.provider      # noqa: F401
import swag_api.resources.services      # noqa: F401
from swag_api.__about__ import (
    __author__, __copyright__, __email__, __license__, __summary__, __title__,
    __url__, __version__
)

__all__ = [
    "__title__", "__summary__", "__url__", "__version__", "__author__",
    "__email__", "__license__", "__copyright__",
]

SWAG_API_BLUEPRINTS = (
    api_bp,
)


def create_app(config=None) -> Flask:
    app = factory.create_app(app_name=__name__, blueprints=SWAG_API_BLUEPRINTS, config=None)
    return app


cli = FlaskGroup(create_app=create_app)
