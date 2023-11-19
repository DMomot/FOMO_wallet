from backend.models import ChainId

native_to_wrapped_mapping = {
    ChainId.ETH: {
        '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
    },
    ChainId.POLYGON: {
        '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee': '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270',
    },
    ChainId.GNOSIS: {},
    ChainId.ARBITRUM: {},
}

wrapped_to_native_mapping = {
    ChainId.ETH: {
        '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2': '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
    },
    ChainId.POLYGON: {
        '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270': '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
    },
    ChainId.GNOSIS: {},
    ChainId.ARBITRUM: {},
}
