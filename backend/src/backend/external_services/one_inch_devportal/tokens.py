import asyncio

import aiohttp

# from aiocache import cached, Cache, multi_cached
# from backend.cache import cache
from backend.models import ChainId, AddressType
from backend.config import settings
from aiohttp_retry import RetryClient, RandomRetry


async def get_tokens_by_chain_id(
        chain_id: ChainId,
):
    async with RetryClient(retry_options=RandomRetry(statuses=[429], attempts=10, min_timeout=1, max_timeout=1)) as client:
        async with client.request(
                "GET",
                f"https://api.1inch.dev/token/v1.2/{chain_id}",
                headers={'Authorization': f'Bearer {settings.one_inch_devportal_api_key}'},
        ) as response:
            tokens: dict[AddressType, dict] = await response.json()
        return tokens


# @cached(cache=Cache.REDIS, namespace="main", client=cache.client)
async def get_tokens():
    tokens_by_chain_id = await asyncio.gather(
        *(
            get_tokens_by_chain_id(chain_id)
            for chain_id in ChainId
        )
    )
    return {
        chain_id: tokens
        for chain_id, tokens in zip(ChainId, tokens_by_chain_id)
    }


if __name__ == '__main__':
    print(asyncio.run(get_tokens()))
