import asyncio

import aiohttp

from backend.models import ChainId, AddressType
from backend.config import settings


async def get_balances_by_chain_id_and_address(
        chain_id: ChainId,
        address: AddressType,
):
    async with aiohttp.request(
            "GET",
            f"https://api.1inch.dev/balance/v1.2/{chain_id}/balances/{address}",
            headers={'Authorization': f'Bearer {settings.one_inch_devportal_api_key}'},
    ) as response:
        print(response)
        balances: dict[AddressType, int] = {k: int(v) for k, v in (await response.json()).items()}
    return balances


async def get_balances_by_address(
        address: AddressType,
) -> dict[ChainId, dict[AddressType, float]]:
    balances_by_chain_id = await asyncio.gather(
        *(
            get_balances_by_chain_id_and_address(chain_id, address)
            for chain_id in ChainId
        )
    )
    return {
        chain_id: balances
        for chain_id, balances in zip(ChainId, balances_by_chain_id)
    }

if __name__ == '__main__':
    print(asyncio.run(get_balances_by_address('0x7b065Fcb0760dF0CEA8CFd144e08554F3CeA73D1')))
