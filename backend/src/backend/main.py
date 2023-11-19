from copy import deepcopy

from fastapi import FastAPI

from backend.external_services.one_inch_devportal.full_info import get_address_info
from backend.models import AddressType
from backend.protocols.aave import AAVE
from fastapi.middleware.cors import CORSMiddleware

from backend.protocols.gearbox import GEARBOX
from backend.protocols.lido import LIDO
from backend.protocols.spark import SPARK
from backend.config import settings

from web3 import AsyncWeb3, AsyncHTTPProvider
w3 = AsyncWeb3(AsyncHTTPProvider(settings.infura_url))

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


def sort_func(address_info):
    if 'fomo' in address_info and len(address_info['fomo']) > 0:
        return max(x['unrealized_value'] for x in address_info['fomo'])
    else:
        return 0


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
                apys: dict | None = await protocol.get_apy(
                    underlying_token_address=token_info['address'],
                    chain_id=token_info['chain_id'],
                )

                if apys:
                    apys_returned = []
                    for apy in deepcopy(apys):
                        unrealized_value = token_info['value'] * apy['apy']
                        if unrealized_value < 100:
                            apy['unrealized_value'] = round(unrealized_value, 2)
                        else:
                            apy['unrealized_value'] = round(unrealized_value)

                        if unrealized_value == 0:
                            continue

                        unrealized_amount = token_info['amount'] * apy['apy']
                        if unrealized_amount < 100:
                            apy['unrealized_amount'] = round(unrealized_amount, 2)
                        else:
                            apy['unrealized_amount'] = round(unrealized_amount)

                        apy['logo_url'] = protocol.get_logo_url()
                        apy['project_url'] = protocol.get_project_url()

                        if (
                                'additional_info' in apy
                                and 'unrealized_value' in apy['additional_info']
                                and callable(apy['additional_info']['unrealized_value'])
                        ):
                            apy['additional_info']['unrealized_value'] = \
                                apy['additional_info']['unrealized_value'](token_info['value'])

                        apys_returned.append(apy)

                    if 'fomo' not in token_info:
                        token_info['fomo'] = apys_returned
                    else:
                        token_info['fomo'] += apys_returned

    # Sorted into token_info by unrealized_value
    for token_info in address_info:
        if 'fomo' in token_info:
            token_info['fomo'] = sorted(token_info['fomo'], key=lambda x: x['unrealized_value'], reverse=True)

    # Sorted by max(fomo.unrealized_value)
    address_info = sorted(
        address_info,
        key=sort_func,
        reverse=True
    )

    return address_info


@app.get("/ens/{name}")
async def get_address_by_ens(name: str):
    return await w3.ens.address(name)
