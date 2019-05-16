"""
.. module: swag_api.plugins.metrics.sample
    :platform: Unix
    :synopsis: This module contains all the needed functions to allow
    the factory app creation.
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Mike Grima <mgrima@netflix.com>
"""
from typing import Dict

from flask import Flask
from swag_api.plugins.metrics import MetricsPlugin


class SamplePlugin(MetricsPlugin):

    def __init__(self, app: Flask):
        """All setup logic here."""
        super().__init__(app)

    def send_counter_metric(self, counter_name: str, tags: Dict[str, str] = None):
        """Send a metric to the metrics collection system that you are making use of."""
        self.app.logger.info(f'Metrics collected for counter: {counter_name}, tags: {tags}')

    def send_latency_metric(self, time_name: str, latency: float, tags: Dict[str, str] = None):
        """Send a metric to the metrics collection system that you are making use of."""
        self.app.logger.info(f'Metrics collected for time metric: {time_name}, value: {latency}, tags: {tags}')
