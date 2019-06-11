# swag-api

![Build Status](https://travis-ci.org/Netflix-Skunkworks/swag-api.svg?branch=master)

[![codecov](https://codecov.io/gh/Netflix-Skunkworks/swag-api/branch/master/graph/badge.svg)](https://codecov.io/gh/Netflix-Skunkworks/swag-api)

![OSS Status](https://img.shields.io/badge/NetflixOSS-active-brightgreen.svg)

This is the API for the [swag-client](https://github.com/Netflix-Skunkworks/swag-client) account metadata service.

## Quickstart

*Frontend*

* Change directories to the `static` directory and run `npm install`
* `npm start`

*Backend*

* `pip install -e .`
* `swag-api run`


## Metrics Plugins

To create a custom metrics plugin, you will need to do the following:

1. Create the following directory structure under `swag_api/plugins/metrics`:

    ```
    swag_api/plugins/metrics/
        ├── ...
        └── your_plugin_here
            ├── __init__.py
            └── module.py
    ```
    
1. A sample plugin is provided in `swag_api/plugins/metrics/sample`. You can enable the sample plugin by setting the Flask configuration `ENABLE_SAMPLE_METRICS_PLUGIN` set to `True`.

1. In your `module.py` you will need to write your plugin to subclass the `MetricsPlugin` found in `swag_api/plugins/metrics/__init__.py`.

    The base class has 2 functions that you need to overwrite: `send_counter_metric`, and `send_latency_metric`. The `counter_metric` 
    is a metric for counting how many times an API is hit. The `latency_metric` is used to gauge the total time it takes to process a given API call.

1. Once you have implemented the `module.py`, in your package's `__init__.py`, you will need to import your plugin `as MetricsPlugin`. See the sample plugin's `__init__.py` for an example.

1. You can have multiple metrics plugins enabled should you want! `swag-api` will look for them on startup and initialize them. Feel free to add any initialization code you need
in your class's `__init__()`.
