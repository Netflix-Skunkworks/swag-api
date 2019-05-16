"""
.. module: swag_api.plugins.metrics
    :platform: Unix
    :synopsis: This module contains all the needed functions to allow
    the factory app creation.
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Mike Grima <mgrima@netflix.com>
"""
from typing import Dict

from flask import Flask


class MetricsPlugin(object):

    def __init__(self, app: Flask):
        """The base MetricsPlugin class. This is what all metrics plugins will need to sub-class of."""
        self.app = app  # This is used to get the application context for use in your plugins.

    def send_counter_metric(self, counter_name: str, tags: Dict[str, str] = None):
        """Send a count-type of metric to the metrics collection system that you are making use of.
        :param counter_name: The name of the counter to send the metric for. This is used for simple
                             checkpointing/counting that this thing was invoked.
        :param tags: A dict of name value pairs for additional metadata to include with the metric.
        """
        raise NotImplementedError()

    def send_latency_metric(self, time_name: str, latency: float, tags: Dict[str, str] = None):
        """Send a time/latency type of metric to the metrics collection system that you are making use of.
        :param time_name: The name of the latency counter to send the metric for. This used to associate
                          the total amount of time it took to do something.
        :param time_value: The latency/amount of time it took for this thing to be completed by.
        :param tags: A dict of name value pairs for additional metadata to include with the metric.
        """
        raise NotImplementedError()


class InvalidPluginConfigurationException(Exception):
    pass


class InvalidPluginClassException(Exception):
    pass
