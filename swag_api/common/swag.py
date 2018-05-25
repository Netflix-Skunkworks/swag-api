from swag_api.extensions import swag


def get_account(account):
    account_data = swag.get("[?id=='{}']".format(account))

    if not account_data:
        account_data = swag.get_by_name(account, alias=True)
        if account_data:
            return account_data[0]

    if not account_data:
        return None

    return account_data
