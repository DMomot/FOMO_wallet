from backend.models import ChainId, AddressType
from backend.protocols.base import BaseProtocol
from backend.protocols.gearbox.cached_data import state_last_month


class GEARBOX(BaseProtocol):
    async def get_supported_tokens(
            self,
            chain_id: ChainId,
    ):
        return [x['underline_token_address'] for x in state_last_month[chain_id]]

    async def get_supported_chains(self):
        return [
            ChainId.ETH,
        ]

    async def get_apy(
            self,
            underline_token_address: AddressType,
            chain_id: ChainId,
    ):
        res = [
            x for x in state_last_month[chain_id]
            if x['underline_token_address'].lower() == underline_token_address.lower()
        ]
        if len(res) == 0:
            return None
        return res[0]
