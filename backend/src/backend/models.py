import re
from enum import IntEnum

from annotated_types import Len, Predicate
from typing import Annotated

AddressType = Annotated[str, Len(min_length=42, max_length=42), Predicate(re.compile("^0x[0-9a-fA-F]*$").search)]


class ChainId(IntEnum):
    ETH = 1
    # POLYGON = 137
    # GNOSIS = 100
    # ARBITRUM = 42161
