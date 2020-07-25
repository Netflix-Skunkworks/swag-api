LOG_LEVEL = "DEBUG"

debug = True

SECRET_KEY = 'supersupersupersecret'

# Disable this in your environment:
ENABLE_SAMPLE_METRICS_PLUGIN = True

# Enable Reverse Proxy support:
SWAG_PROXIES = {
    'x_for': 1,
    'x_proto': 1,
    'x_host': 1,
    'x_port': 0,
    # 'x_prefix': 0  # This should default to 0 in the test.
}
