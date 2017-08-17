"""
swag-api
========

Web interface for SWAG data.

:copyright: (c) 2017 by Netflix, see AUTHORS for more
:license: Apache, see LICENSE for more details.
"""
import os
from setuptools import setup, find_packages

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))

about = {}
with open(os.path.join(ROOT, 'swag_api', '__about__.py')) as f:
    exec(f.read(), about)  # nosec: about file is benign

setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__email__"],
    url=about["__uri__"],
    description=about["__summary__"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask==0.12.2',
        'raven[flask]==6.1.0',
        'swag_client==0.2.3',
        'Flask-RESTful==0.3.6',
        'gunicorn==19.7.1'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'swag-api=swag_api:cli.main',
        ]
    }
)
