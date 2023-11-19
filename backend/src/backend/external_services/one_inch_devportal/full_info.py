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
    result = []
    for chain_id, chain_tokens in tokens.items():
        for token_address, token_info in chain_tokens.items():
            if balances[chain_id].get(token_address) and 'logoURI' in token_info:
                price = spot_prices[chain_id].get(token_address) or 0
                value = round(balances[chain_id][token_address] / (10 ** token_info["decimals"]) * price)
                amount = balances[chain_id][token_address] / (10 ** token_info["decimals"])
                if amount < 100:
                    amount = round(amount, 2)
                else:
                    amount = round(amount)
                result.append({
                    "chain_id": chain_id,
                    "address": token_address,
                    "name": token_info["name"],
                    "symbol": token_info["symbol"],
                    "amount_raw": balances[chain_id][token_address],
                    "amount": amount,
                    "price": price,
                    "value": value,
                    "logo_url": token_info["logoURI"],
                    "decimals": token_info["decimals"],
                })

    return list(sorted(result, key=lambda x: x["value"], reverse=True))


if __name__ == '__main__':
    print(asyncio.run(get_address_info('0x7b065Fcb0760dF0CEA8CFd144e08554F3CeA73D1')))
