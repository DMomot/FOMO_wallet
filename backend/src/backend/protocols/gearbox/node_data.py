from uuid import uuid4
from web3 import Web3
from web3 import HTTPProvider
from backend.web3_provider import MyHTTPProvider

from backend.protocols.gearbox.contracts import GEARBOX_CONTRACTS


def to_lp(node_provider, gearbox_contract, block_number, amount):
    four_bytes = '0x4d778ad1'
    request = dict(
        jsonrpc='2.0',
        method='eth_call',
        params=[
            {
                'to': gearbox_contract,
                'data': four_bytes + hex(amount)[2:].zfill(64)
            },
            hex(block_number)
        ],
        id=uuid4().hex
    )
    res = node_provider.send([request])
    liquidity = int(res[0]['result'], 16)
    return liquidity


def from_lp(node_provider, gearbox_contract, block_number, liquidity):
    four_bytes = '0x5427c938'
    request = dict(
        jsonrpc='2.0',
        method='eth_call',
        params=[
            {
                'to': gearbox_contract,
                'data': four_bytes + hex(liquidity)[2:].zfill(64)
            },
            hex(block_number)
        ],
        id=uuid4().hex
    )
    res = node_provider.send([request])
    amount = int(res[0]['result'], 16)
    return amount


def get_gear_token_apy(node_provider, gearbox_contract, block_number, currency, reward_base, price):
    four_bytes = '0xfe14112d'
    req = dict(
        jsonrpc='2.0',
        method='eth_call',
        params=[
            {
                'to': gearbox_contract,
                'data': '0xfe14112d' + ''.zfill(64)
            },
            hex(block_number)
        ],
        id=uuid4().hex
    )
    res = node_provider.send([req])
    el = int(res[0]['result'], 16)

    timescale = 5*60*24*365
    # print(reward_base, timescale, prices["usdc"], )
    apy = reward_base * timescale * price / el

    return apy


def get_aprs(node_provider, block_number_previous, block_number_current, gearbox_contracts):
    records = []

    for k, v in gearbox_contracts.items():
        liqudity = to_lp(node_provider, v["gearbox"], block_number_previous, v["amount"])
        amount1 = from_lp(node_provider, v["gearbox"], block_number_current, liqudity)
        r = 12 * (amount1 / v["amount"] - 1)
        apy = (1 + r / 31536000) ** 31536000 - 1

        if apy < 0:
            apy = 0

        apy_gearbox = get_gear_token_apy(node_provider, v["gearbox"], block_number_current, k, v["reward"], v["price"])

        record = {
            "chain_id": 1,
            "protocol_name": "GEARBOX",
            "underlying_token_address": v["underlying"].lower(),
            "apy": '{:.16f}'.format(apy),
            "additional_parameters": {"apy_gearbox": '{:.16f}'.format(apy_gearbox)}
        }
        records.append(record)
    return records


def make_cache():
    w3 = Web3(HTTPProvider("https://eth-mainnet.g.alchemy.com/v2/7t0ETmbK3sb6zwa2PBX-OdS9Pouq94xV"))
    block_number_current = int(w3.eth.get_block('latest').number) - 64
    eth_month_gap = 220_000
    block_number_previous = block_number_current - eth_month_gap

    node_provider = MyHTTPProvider("https://eth-mainnet.g.alchemy.com/v2/7t0ETmbK3sb6zwa2PBX-OdS9Pouq94xV")
    return get_aprs(node_provider, block_number_previous, block_number_current, GEARBOX_CONTRACTS)
