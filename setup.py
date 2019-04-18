"""
swag-api
========

Web interface for SWAG data.

:copyright: (c) 2017 by Netflix, see AUTHORS for more
:license: Apache, see LICENSE for more details.
"""
import os

from setuptools import find_packages, setup

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
        'tests': tests_requires
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
