from backend.models import ChainId
from backend.utils import send_request, hex_to_int


def make_cache(chain_id: ChainId):
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
            'chain_id': 1,
            'protocol_name': 'LIDO',
            'underlying_token_address': underlying_token_address.lower(),
            'apy': "{:.16f}".format(apy)
        })

    return records
