import asyncio

from backend.cache import momoized_async
from backend.logger import log
from backend.models import ChainId, AddressType
from backend.config import settings
from aiohttp_retry import RetryClient, RandomRetry


async def get_tokens_by_chain_id(
        chain_id: ChainId,
):
    async with RetryClient(
            retry_options=RandomRetry(statuses=[429], attempts=10, min_timeout=1, max_timeout=1),
            logger=log,
    ) as client:
        async with client.request(
                "GET",
                f"https://api.1inch.dev/token/v1.2/{chain_id}",
                headers={'Authorization': f'Bearer {settings.one_inch_devportal_api_key}'},
        ) as response:
            log.info(f"spot_price", status=response.status, chain_id=chain_id, url=response.url)
            tokens: dict[AddressType, dict] = await response.json()
        return tokens


@momoized_async()
async def get_tokens():
    tokens_by_chain_id = await asyncio.gather(
        *(
            get_tokens_by_chain_id(chain_id)
            for chain_id in ChainId
        )
    )
    print('not cached')
    return {
        chain_id: tokens
        for chain_id, tokens in zip(ChainId, tokens_by_chain_id)
    }


if __name__ == '__main__':

    async def main():
        for x in range(10):
            await asyncio.sleep(x)
            t = await get_tokens()
            print('keys: ', t.keys())

    asyncio.run(main())
    # print(x.keys())
