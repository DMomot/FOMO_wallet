from fastapi import FastAPI

from backend.models import AddressType

app = FastAPI()


@app.get("/")
async def f(
        address: AddressType = '0x7b065Fcb0760dF0CEA8CFd144e08554F3CeA73D1',
):
    ...
