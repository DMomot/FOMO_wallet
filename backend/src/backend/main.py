from fastapi import FastAPI

from backend.external_services.one_inch_devportal.full_info import get_address_info
from backend.models import AddressType

app = FastAPI()


@app.get("/{address}")
async def get_fomo(
    address: AddressType,
):
    return await get_address_info(address=address)
