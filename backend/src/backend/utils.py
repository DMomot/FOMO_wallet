from web3.auto import Web3
from web3.middleware import geth_poa_middleware
import requests
import json


def hex_to_int(x):
    if x is not None:
        assert isinstance(x, str), f"Expected hex string, got {type(x)}"
        if x in ("0x", ""):
            return None
        return int(x, 16)
    else:
        return None


def send_request(chain_id, contract_address, data, block_number):
    if chain_id == 1:
        node_address = 'https://eth-mainnet.g.alchemy.com/v2/7t0ETmbK3sb6zwa2PBX-OdS9Pouq94xV'
        w3 = Web3(Web3.HTTPProvider(node_address))
        block_number_delta = 220_000
    elif chain_id == 137:
        node_address = 'https://polygon-mainnet.g.alchemy.com/v2/hFeeeDTV-4tpKPrCml4oxMtL4IW6u7a_'
        w3 = Web3(Web3.HTTPProvider(node_address))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        block_number_delta = 1_200_000
    elif chain_id == 42161:
        node_address = 'https://arb-mainnet.g.alchemy.com/v2/bGF2nATaHtvNF1YteY0w1hQWcf-cSeBw'
        w3 = Web3(Web3.HTTPProvider(node_address))
        block_number_delta = 10_000_000
    else:
        raise ValueError(f'{chain_id} is not supported')

    if block_number == 'latest':
        block_number = w3.eth.get_block('latest')['number'] - 64
    else:
        block_number = w3.eth.get_block('latest')['number'] - block_number_delta

    data = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [
            {
                "to": contract_address,
                "data": data
            },
            hex(block_number)
        ],
        "id": 1
    }

    response = requests.post(
        node_address,
        data=json.dumps(data)
    ).content

    return json.loads(response)