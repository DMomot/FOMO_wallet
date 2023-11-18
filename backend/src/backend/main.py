from fastapi import FastAPI

from backend.external_services.one_inch_devportal.full_info import get_address_info
from backend.models import AddressType
from backend.protocols.aave import AAVE
from fastapi.middleware.cors import CORSMiddleware

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
]


@app.get("/{address}")
async def get_fomo(
    address: AddressType,
):
    address_info = await get_address_info(address=address)
    for token_address, token_info in address_info.items():
        for protocol in supported_protocols:
            if token_address in await protocol.get_supported_tokens(chain_id=token_info['chain_id']):
                protocol_info: dict | None = await protocol.get_apy(
                    underline_token_address=token_address,
                    chain_id=token_info['chain_id'],
                )
                if protocol_info:
                    protocol_info['unrealized_value'] = token_info['value'] * (protocol_info['apy'] / 12)
                    if 'fomo' not in token_info:
                        token_info['fomo'] = [protocol_info]
                    else:
                        token_info['fomo'].append(protocol_info)
    return address_info
