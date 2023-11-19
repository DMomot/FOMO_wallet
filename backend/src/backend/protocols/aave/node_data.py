from backend.protocols.aave.contracts import AAVE_FACTORY, AAVE_LENDING_POOLS
from backend.utils import send_request, hex_to_int


def make_cache():
    records = []
    for lending_pool in AAVE_LENDING_POOLS:
        contract_address = lending_pool['contract_address']
        protocol = lending_pool['protocol']
        chain_id = lending_pool['chain_id']

        for pool in AAVE_FACTORY:
            if chain_id == pool['chain_id'] and protocol == pool['protocol']:
                underlying_token_address = pool['address']

                data = '0xd15e0053' + underlying_token_address[2:].zfill(64)

                current_res_request = send_request(chain_id, contract_address, data, 'latest')
                current_res = hex_to_int(current_res_request['result'])

                previous_res_request = send_request(chain_id, contract_address, data, '1month ago')
                previous_res = hex_to_int(previous_res_request['result'])

                if current_res and previous_res:

                    r = 12 * (current_res / previous_res - 1)
                    timescale = 31536000
                    apy = (1 + r / timescale) ** timescale - 1

                    records.append(
                        {
                            'chain_id': chain_id,
                            'protocol_name': protocol,
                            'underlying_token_address': underlying_token_address.lower(),
                            'apy': '{:.16f}'.format(apy),
                        }
                    )

    return records
