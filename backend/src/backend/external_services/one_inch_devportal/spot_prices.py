# https://api.1inch.dev/price/v1.1/1
import asyncio

import aiohttp

from backend.models import ChainId, AddressType
from backend.config import settings


async def get_spot_prices_by_chain_id(
        chain_id: ChainId,
):
    async with aiohttp.request(
            "GET",
            f"https://api.1inch.dev/price/v1.1/{chain_id}",
            headers={'Authorization': f'Bearer {settings.one_inch_devportal_api_key}'},
    ) as response:
        spot_prices: dict[AddressType, int] = {k: int(v) for k, v in (await response.json()).items()}
    return spot_prices


async def get_spot_prices() -> dict[ChainId, dict[AddressType, float]]:
    balances_by_chain_id = asyncio.gather(
        *(
            get_spot_prices_by_chain_id(chain_id)
            for chain_id in ChainId
        )
    )
    return {
        chain_id: balances
        for chain_id, balances in zip(ChainId, balances_by_chain_id)
    }
