"""
.. module: swag_api.common.swag
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Will Bengtson <wbengtson@netflix.com>
"""
from swag_api.extensions import swag


def get_account(account: str) -> dict:
    account_data = swag.get("[?id=='{}']".format(account))

    if not account_data:
        account_data = swag.get_by_name(account, alias=True)
        if account_data:
            return account_data[0]

    if not account_data:
        return None

    return account_data
