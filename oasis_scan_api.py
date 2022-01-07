import requests
import json


def get_wallet_info(address):
    # get data from API
    response = requests.get('https://api.oasisscan.com/mainnet/chain/account/info/' + str(address))

    # extract data as dictionary from response
    parsed_json = (json.loads(response.text))
    data = parsed_json['data']

    # turn dictionary in message
    message = ''
    for k, i in data.items():
        message += '{0} = {1}\n'.format(k, i)

    return message
