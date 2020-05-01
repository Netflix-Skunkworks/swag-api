"""
swag-api
========

Web interface for SWAG data (see swag-client for details).

:copyright: (c) 2020 by Netflix, see AUTHORS for more
:license: Apache, see LICENSE for more details.
"""
import os

from setuptools import setup

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))

about = {}
with open(os.path.join(ROOT, 'swag_api', '__about__.py')) as f:
    exec(f.read(), about)  # nosec: about file is benign

setup(
    name="swag-api",
    description=about["__summary__"],
    setup_requires="setupmeta",
    entry_points={
        'console_scripts': [
            'swag-api=swag_api:cli.main',
        ]
    }
)
