from backend.models import ChainId
from backend.utils import send_request, hex_to_int


def make_cache_eth(chain_id: ChainId):
    assert chain_id == ChainId.ETH
    records = []
    contract_address = '0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0'
    underlying_token_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
    data = '0x035faf82'  # getReserveNormalizedIncome(address)

    current_res_request = send_request(chain_id, contract_address, data, 'latest')
    current_res = hex_to_int(current_res_request['result'])

    previous_res_request = send_request(chain_id, contract_address, data, '1monthago')
    previous_res = hex_to_int(previous_res_request['result'])

    if current_res and previous_res:
        apr = ((12 * (current_res / previous_res - 1)))
        apy = (pow((1 + (apr) / 31536000), 31536000) - 1)

        records.append({
            'chain_id': chain_id,
            'protocol_name': 'LIDO',
            'underlying_token_address': underlying_token_address.lower(),
            'apy': "{:.16f}".format(apy)
        })

    return records


def make_cache_polygon(chain_id: ChainId):
    records = []
    contract_address = '0xdEd6C522d803E35f65318a9a4d7333a22d582199'
    underlying_token_address = '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270'

    data = '0x679aefce' #getRate()

    current_res_request = send_request(chain_id, contract_address, data, 'latest')
    current_res = hex_to_int(current_res_request['result'])

    previous_res_request = send_request(chain_id, contract_address, data, '1monthago')
    previous_res = hex_to_int(previous_res_request['result'])

    if current_res and previous_res:
        apr = ((12 * (current_res / previous_res - 1)))
        apy = (pow((1 + (apr) / 31536000), 31536000) - 1)

        records.append({
            'chain_id': chain_id,
            'protocol_name': 'LIDO',
            'underlying_token_address': underlying_token_address.lower(),
            'apy': "{:.16f}".format(apy)
        })
    return records
