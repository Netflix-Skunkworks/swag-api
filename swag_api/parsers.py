"""
.. module: swag_api.parsers
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. author:: Will Bengtson <wbengtson@netflix.com>
"""
# Add request parsers to document the API in SWAGGER and do nice auto required field parsing in REST API
from flask_restx import reqparse

namespace_arguments = reqparse.RequestParser()
namespace_arguments.add_argument('namespace', type=str, help='Namespace for SWAG (ex. accounts)')

env_arguments = reqparse.RequestParser()
env_arguments.add_argument('namespace', type=str, help='Namespace for SWAG (ex. accounts)')
env_arguments.add_argument('env', type=str, help='Environment (ex. prod or test)')

owner_arguments = reqparse.RequestParser()
owner_arguments.add_argument('namespace', type=str, help='Namespace for SWAG (ex. accounts)')
owner_arguments.add_argument('owner', type=str, help='Owner of account (ex. ABC Company)')

provider_arguments = reqparse.RequestParser()
provider_arguments.add_argument('namespace', type=str, help='Namespace for SWAG (ex. accounts)')
provider_arguments.add_argument('provider', type=str, help='Provider of the account (ex. aws)')

account_arguments = reqparse.RequestParser()
account_arguments.add_argument('namespace', type=str, help='Namespace for SWAG (ex. accounts)')
account_arguments.add_argument('account', type=str, help='Name or ID of account')

account_id_arguments = reqparse.RequestParser()
account_id_arguments.add_argument('namespace', type=str, help='Namespace for SWAG (ex. accounts)')
account_id_arguments.add_argument('account', type=str, help='ID of account')

account_status_arguments = reqparse.RequestParser()
account_status_arguments.add_argument('namespace', type=str, help='Namespace for SWAG (ex. accounts)')
account_status_arguments.add_argument('account_status', type=str, help='Account status (ex. ready)')

service_simple_arguments = reqparse.RequestParser()
service_simple_arguments.add_argument('namespace', type=str, help='Namespace for SWAG (ex. accounts)')
service_simple_arguments.add_argument('service', type=str, help='Name of service')

service_account_arguments = reqparse.RequestParser()
service_account_arguments.add_argument('namespace', type=str, help='Namespace for SWAG (ex. accounts)')
service_account_arguments.add_argument('account', type=str, help='Name or ID of account')
service_account_arguments.add_argument('service_name', type=str, help='Name of service')

service_region_arguments = reqparse.RequestParser()
service_region_arguments.add_argument('namespace', type=str, help='Namespace for SWAG (ex. accounts)', location='args')
service_region_arguments.add_argument('account', type=str, help='Name or ID of account', location='args')
service_region_arguments.add_argument('service_name', type=str, help='Name of service', location='args')
service_region_arguments.add_argument('enabled', type=bool, required=True, help='True of False', location='json')
service_region_arguments.add_argument('region', type=str, help='Region to enable of "all" for all regions',
                                      location='json')
