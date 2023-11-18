from backend.models import ChainId

state_last_month = {
    ChainId.ETH: [
        {
            "chain_id": 1,
            "protocol_name": "GEARBOX",
            "underline_token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
            "apy": 0.0044498683043550,
            "additional_info": {
                "description": "APY / Unrealized value in GEAR tokens",
                "token_address": "0xba3335588d9403515223f109edc4eb7269a9ab5d",
                "apy_in_gear_tokens": 0.0922970446205191,
                "unrealized_value": lambda value: value * (0.0922970446205191),
            },
        },
        {
            "chain_id": 1,
            "protocol_name": "GEARBOX",
            "underline_token_address": "0x24946bcbbd028d5abb62ad9b635eb1b1a67af668",
            "apy": 0.0040174116509912,
            "additional_info": {
                "description": "APY / Unrealized value in GEAR tokens",
                "token_address": "0xba3335588d9403515223f109edc4eb7269a9ab5d",
                "apy_in_gear_tokens": 0.0976843737267312,
                "unrealized_value": lambda value: value * (0.0976843737267312),
            },
        },
        {
            "chain_id": 1,
            "protocol_name": "GEARBOX",
            "underline_token_address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            "apy": 0.0094212180037720,
            "additional_info": {
                "description": "APY / Unrealized value in GEAR tokens",
                "token_address": "0xba3335588d9403515223f109edc4eb7269a9ab5d",
                "apy_in_gear_tokens": 0.0410118213941159,
                "unrealized_value": lambda value: value * (0.0410118213941159),
            },
        },
        {
            "chain_id": 1,
            "protocol_name": "GEARBOX",
            "underline_token_address": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
            "apy": 0.0000000000000000,
            "additional_info": {
                "description": "APY / Unrealized value in GEAR tokens",
                "token_address": "0xba3335588d9403515223f109edc4eb7269a9ab5d",
                "apy_in_gear_tokens": 0.0301588247505191,
                "unrealized_value": lambda value: value * (0.0301588247505191),
            },
        },
    ]
}
