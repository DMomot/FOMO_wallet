from fastapi import FastAPI

from backend.external_services.one_inch_devportal.full_info import get_address_info
from backend.models import AddressType
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    # openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{address}")
async def get_fomo(
    address: AddressType,
):
    return await get_address_info(address=address)
