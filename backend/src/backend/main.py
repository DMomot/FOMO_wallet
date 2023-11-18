from fastapi import FastAPI

from backend.external_services.one_inch_devportal.full_info import get_address_info
from backend.models import AddressType
from backend.protocols.aave import AAVE
from fastapi.middleware.cors import CORSMiddleware

from backend.protocols.gearbox import GEARBOX

app = FastAPI(
    # openapi_url="/api/openapi.json",
)

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
]


@app.get("/{address}")
async def get_fomo(
    address: AddressType,
):
    address_info = await get_address_info(address=address)

    # Add fomo
    for token_address, token_info in address_info.items():
        for protocol in supported_protocols:
            if token_address in await protocol.get_supported_tokens(chain_id=token_info['chain_id']):
                protocol_info: dict | None = await protocol.get_apy(
                    underline_token_address=token_address,
                    chain_id=token_info['chain_id'],
                )
                if protocol_info:
                    protocol_info['unrealized_value'] = token_info['value'] * (protocol_info['apy'] / 12)
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

    # Sorted by unrealized_value
    for token_address, token_info in address_info.items():
        if 'fomo' in token_info:
            token_info['fomo'] = sorted(token_info['fomo'], key=lambda x: x['unrealized_value'], reverse=True)

    return address_info
