from oneinch_py import OneInchSwap, TransactionHelper, OneInchOracle

from backend.config import node_urls
from backend.models import ChainId, AddressType


def get_spot_price(
    chain_id: ChainId,
    src_token: AddressType,
    dst_token: AddressType,
    src_token_decimal: int = 18,
    dst_token_decimal: int = 18,
):
    oracle = OneInchOracle(node_urls[chain_id], chain='ethereum')
    return oracle.get_rate(
        src_token=src_token,
        dst_token=dst_token,
        src_token_decimal=src_token_decimal,
        dst_token_decimal=dst_token_decimal,
    )

