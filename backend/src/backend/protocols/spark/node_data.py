from uuid import uuid4

from backend.protocols.spark.contracts import SPARK_CONTRACTS
from backend.utils import get_node_provider


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


def make_cache():
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

            records.append({
                "chain_id": chain_id,
                "protocol_name": "SPARK",
                "underlying_token_address": contract["underlying"].lower(),
                'apy': '{:.16f}'.format(apy)
            })

    return records
