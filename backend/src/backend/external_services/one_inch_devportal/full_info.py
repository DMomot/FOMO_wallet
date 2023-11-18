import asyncio

from backend.external_services.one_inch_devportal.balances import get_balances_by_address
from backend.external_services.one_inch_devportal.tokens import get_tokens
from backend.external_services.one_inch_devportal.spot_prices import get_spot_prices
from backend.models import AddressType


async def get_address_info(
        address: AddressType,
):
    balances, tokens, spot_prices = await asyncio.gather(
        *(
            get_balances_by_address(address),
            get_tokens(),
            get_spot_prices()
        )
    )
    # Too many requests to 1inch API =(
