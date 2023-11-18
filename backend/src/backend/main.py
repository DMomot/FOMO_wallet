from fastapi import FastAPI

from backend.external_services.one_inch_devportal.full_info import get_address_info
from backend.models import AddressType
from backend.protocols.aave import AAVE
from fastapi.middleware.cors import CORSMiddleware

from backend.protocols.gearbox import GEARBOX
from backend.protocols.lido import LIDO
from backend.protocols.spark import SPARK

from web3 import AsyncWeb3, AsyncHTTPProvider
w3 = AsyncWeb3(AsyncHTTPProvider('https://mainnet.infura.io/v3/ce3a8e24ad4f4ea78dede1bbf11e436b'))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


supported_protocols = [
    AAVE(),
    GEARBOX(),
    SPARK(),
    LIDO(),
]


@app.get("/fomo/{address}")
async def get_fomo_last_month(
    address: AddressType,
):
    address_info = await get_address_info(address=address)

    # Add fomo
    for token_info in address_info:
        for protocol in supported_protocols:
            if (
                    token_info['chain_id'] in await protocol.get_supported_chains()
                    and token_info['address'] in await protocol.get_supported_tokens(chain_id=token_info['chain_id'])
            ):
                protocol_info: dict | None = await protocol.get_apy(
                    underlying_token_address=token_info['address'],
                    chain_id=token_info['chain_id'],
                )
                if protocol_info:
                    protocol_info['unrealized_value'] = token_info['value'] * (protocol_info['apy'])
                    protocol_info['unrealized_amount'] = token_info['amount'] * (protocol_info['apy'])
                    protocol_info['logo_url'] = protocol.get_logo_url()
                    protocol_info['project_url'] = protocol.get_project_url()

                    if (
                            'additional_info' in protocol_info
                            and 'unrealized_value' in protocol_info['additional_info']
                            and callable(protocol_info['additional_info']['unrealized_value'])
                    ):
                        protocol_info['additional_info']['unrealized_value'] = \
                            protocol_info['additional_info']['unrealized_value'](token_info['value'])

                    if 'fomo' not in token_info:
                        token_info['fomo'] = [protocol_info]
                    else:
                        token_info['fomo'].append(protocol_info)

    # Sorted into token_info by unrealized_value
    for token_info in address_info:
        if 'fomo' in token_info:
            token_info['fomo'] = sorted(token_info['fomo'], key=lambda x: x['unrealized_value'], reverse=True)

    # Sorted by max(fomo.unrealized_value)
    address_info = sorted(
        address_info,
        key=lambda x: max(x['unrealized_value'] for x in x.get('fomo', [{'unrealized_value': 0}])),
        reverse=True
    )

    return address_info


@app.get("/ens/{name}")
async def get_address_by_ens(name: str):
    return await w3.ens.address(name)
