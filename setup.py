"""
swag-api
========

Web interface for SWAG data.

:copyright: (c) 2017 by Netflix, see AUTHORS for more
:license: Apache, see LICENSE for more details.
"""
import os
from setuptools import setup, find_packages

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
try:  # for pip >= 10
    from pip._internal.download import PipSession
except ImportError:  # for pip <= 9.0.3
    from pip.download import PipSession


ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))

about = {}
with open(os.path.join(ROOT, 'swag_api', '__about__.py')) as f:
    exec(f.read(), about)  # nosec: about file is benign


install_requires = [
    'flask>=0.12.2',
    'raven[flask]>=6.1.0',
    'swag_client>=0.3.5',
    'flask-restplus>=0.11.0',
    'gunicorn>=19.7.1',
    'flask-cors>=3.0.3'
]


tests_require = [
    'pytest>==3.0.6',
    'moto>=1.0.1',
    'coveralls>=1.1'
]


# Gather install requirements from requirements.txt
install_reqs = parse_requirements('requirements.txt', session=PipSession())
install_requires = [str(ir.req) for ir in install_reqs]

# Gather test requirements from requirements-test.txt
test_reqs = parse_requirements('requirements-test.txt', session=PipSession())
tests_requires = [str(tr.req) for tr in test_reqs]


setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__email__"],
    url=about["__uri__"],
    description=about["__summary__"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'tests': tests_require
    },
    setup_requires=[
        'pytest-runner',
    ],
    entry_points={
        'console_scripts': [
            'swag-api=swag_api:cli.main',
        ]
    }
)
