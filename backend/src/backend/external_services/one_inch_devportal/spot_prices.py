import asyncio

from aiohttp_retry import RetryClient, RandomRetry

from backend.cache import momoized_async
from backend.models import ChainId, AddressType
from backend.config import settings
from backend.logger import log


@momoized_async(ttl=60 * 10)
async def get_spot_prices_by_chain_id(
        chain_id: ChainId,
):
    async with RetryClient(
            retry_options=RandomRetry(statuses=[429], attempts=10, min_timeout=0.5, max_timeout=0.5),
            logger=log,
    ) as client:
        async with client.request(
                "GET",
                f"https://api.1inch.dev/price/v1.1/{chain_id}",
                headers={'Authorization': f'Bearer {settings.one_inch_devportal_api_key}'},
                params={"currency": "USD"},
        ) as response:
            log.info(f"spot_price", status=response.status, chain_id=chain_id, url=response.url)
            spot_prices: dict[AddressType, float] = {k: float(v) for k, v in (await response.json()).items()}
    return spot_prices


async def get_spot_prices() -> dict[ChainId, dict[AddressType, float]]:
    balances_by_chain_id = await asyncio.gather(
        *(
            get_spot_prices_by_chain_id(chain_id)
            for chain_id in ChainId
        )
    )
    return {
        chain_id: balances
        for chain_id, balances in zip(ChainId, balances_by_chain_id)
    }


if __name__ == '__main__':
    print(asyncio.run(get_spot_prices()))
