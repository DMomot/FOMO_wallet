from uuid import uuid4
from web3 import Web3, HTTPProvider
from backend.web3_provider import MyHTTPProvider

from backend.protocols.spark.contracts import SPARK_CONTRACTS


def get_liquidity_index(node_provider, contract_address, underlying_token, block_number):
    four_bytes = '0xd15e0053'
    req = dict(
        method='eth_call',
        params=[
            {
                'to': contract_address,
                'data': four_bytes + underlying_token[2:].zfill(64)
            },
            hex(block_number),
        ],
        id=uuid4().hex
    )
    res = node_provider.send([req])
    liquidity_index = int(res[0]['result'], 16)
    return liquidity_index


def get_node_provider(chain_id):
    if chain_id == 1:
        node_address = 'https://eth-mainnet.g.alchemy.com/v2/7t0ETmbK3sb6zwa2PBX-OdS9Pouq94xV'
        w3 = Web3(HTTPProvider(node_address))
        node_provider = MyHTTPProvider(node_address)
        block_number_current = int(w3.eth.get_block('latest').number) - 64
        block_number_delta = 220_000
        block_number_previous = block_number_current - block_number_delta
    elif chain_id == 100:
        node_address = 'https://rpc.xdaichain.com/'
        w3 = Web3(HTTPProvider(node_address))
        node_provider = MyHTTPProvider(node_address)
        block_number_current = int(w3.eth.get_block('latest').number) - 64
        block_number_delta = 500_000
        block_number_previous = block_number_current - block_number_delta
    else:
        raise ValueError(f'{chain_id} is not supported')
    return node_provider, block_number_current, block_number_previous


def execute():
    records = []
    for chain_id, contracts in SPARK_CONTRACTS.items():
        for contract in contracts:
            print(contract)
            node_provider, block_number_current, block_number_previous = get_node_provider(chain_id)
            liquidity_index_previous = get_liquidity_index(node_provider, contract["spark"], contract["underlying"], block_number_previous)
            liquidity_index_current = get_liquidity_index(node_provider, contract["spark"], contract["underlying"], block_number_current)
            if liquidity_index_previous == 0 or liquidity_index_current == 0:
                continue
            r = 12 * (liquidity_index_current / liquidity_index_previous - 1)
            timescale = 31536000
            apy = (1 + r / timescale) ** timescale - 1

            records.append(
                {
                    "chain_id": chain_id,
                    "protocol_name": "SPARK",
                    "underlying_token_address": contract["underlying"].lower(),
                    'apy': '{:.16f}'.format(apy)
                }
            )

    return records
