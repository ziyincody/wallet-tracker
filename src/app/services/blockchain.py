import requests


PREFIX = 'https://blockchain.info'

class APIFailure(Exception):
    pass

def get_single_address_info(address: str):
    try:
        resp = requests.get(
            f'{PREFIX}/rawaddr/{address}'
        )
    except Exception as e:
        raise APIFailure(str(e))

    return resp.json()

