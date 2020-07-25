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


## Special Configuration
This section covers other configuration options that are of importance.

### Reverse Proxy Configuration
If you are using a reverse proxy, like Apache or NGINX to front swag-api, then you will need to set the `SWAG_PROXIES` configuration value in your configuration file.
This is required to prevent a situation where Swagger attempts to load it's data via HTTP instead of HTTPS resulting in a mixed-content error.

`SWAG_PROXIES` is a dictionary (`Dict[str, int]`) that takes in the values that werkzeug provides for the [ProxyFix](https://werkzeug.palletsprojects.com/en/1.0.x/middleware/proxy_fix/#x-forwarded-for-proxy-fix) middleware.
Here is an example that is sufficient to make Swagger happy:

```python
SWAG_PROXIES = {
    'x_for': 1,  # These values should 1 or 0
    'x_host': 1,
}

# The full list of values as documented in https://werkzeug.palletsprojects.com/en/1.0.x/middleware/proxy_fix/#x-forwarded-for-proxy-fix are:
# x_for – Number of values to trust for X-Forwarded-For.
# x_proto – Number of values to trust for X-Forwarded-Proto.
# x_host – Number of values to trust for X-Forwarded-Host.
# x_port – Number of values to trust for X-Forwarded-Port.
# x_prefix – Number of values to trust for X-Forwarded-Prefix.
```

If you are not using a reverse proxy, then you can ingore this section.
