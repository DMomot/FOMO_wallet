from backend.models import ChainId, AddressType
from backend.native_wrapped import native_to_wrapped_mapping
from backend.protocols.base import BaseProtocol
from backend.protocols.gearbox.cached_data import state_last_month


class GEARBOX(BaseProtocol):
    def get_logo_url(self) -> str:
        return 'https://icons.llamao.fi/icons/protocols/gearbox?w=128&h=128'

    def get_project_url(self) -> str:
        return 'https://app.gearbox.fi/pools/'

    async def get_supported_tokens(
            self,
            chain_id: ChainId,
    ) -> set:
        supported_tokens = [x['underlying_token_address'] for x in state_last_month[chain_id]]
        if chain_id in native_to_wrapped_mapping:
            supported_tokens += list(native_to_wrapped_mapping[chain_id].keys())
        return set(supported_tokens)

    async def get_supported_chains(self) -> list:
        return state_last_month.keys()

    async def get_apy(
            self,
            underlying_token_address: AddressType,
            chain_id: ChainId,
    ) -> list | None:
        if underlying_token_address in native_to_wrapped_mapping[chain_id]:
            underlying_token_address = native_to_wrapped_mapping[chain_id][underlying_token_address]

        res = [
            x for x in state_last_month[chain_id]
            if x['underlying_token_address'].lower() == underlying_token_address.lower()
        ]
        if len(res) == 0:
            return None
        return res.copy()
