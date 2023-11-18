import asyncio

import aiohttp

# from aiocache import cached, Cache, multi_cached
# from backend.cache import cache
from backend.models import ChainId, AddressType
from backend.config import settings


async def get_tokens_by_chain_id(
        chain_id: ChainId,
):
    async with aiohttp.request(
            "GET",
            f"https://api.1inch.dev/token/{chain_id}",
            headers={'Authorization': f'Bearer {settings.one_inch_devportal_api_key}'},
    ) as response:
        tokens: dict[AddressType, int] = {k: int(v) for k, v in (await response.json()).items()}
    return tokens


# @cached(cache=Cache.REDIS, namespace="main", client=cache.client)
async def get_tokens():
    tokens_by_chain_id = await asyncio.gather(
        *(
            get_tokens_by_chain_id(chain_id)
            for chain_id in ChainId
        )
    )
    print('ok')
    return {
        chain_id: tokens
        for chain_id, tokens in zip(ChainId, tokens_by_chain_id)
    }


# if __name__ == '__main__':
#     asyncio.run(get_tokens())
