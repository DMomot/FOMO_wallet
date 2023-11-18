export const prepareNativeResult = (chain, result) => {
    let response = {};
    if (chain == 'eth') {
        response = {"chain": "eth",
                    "token_address": "0x0000000000000000000000000000000000000000",
                    "symbol": "ETH",
                    "name": "Ethereum",
                    "decimals": 18,
                    "balance": result.balance,
                    "logo": "https://w7.pngwing.com/pngs/268/1013/png-transparent-ethereum-eth-hd-logo-thumbnail.png",
                    "possible_spam": false,
                    "thumbnail": "https://w7.pngwing.com/pngs/268/1013/png-transparent-ethereum-eth-hd-logo-thumbnail.png"};  
        return response;
    }
    else if (chain == 'polygon') {
        response = {"chain": "polygon",
                    "token_address": "0x0000000000000000000000000000000000001010",
                    "symbol": "MATIC",
                    "name": "Matic Token",
                    "decimals": 18,
                    "balance": result.balance,
                    "logo": "https://i.pinimg.com/originals/9b/1e/97/9b1e977d00b5d887608b156705a10759.png",
                    "possible_spam": false,
                    "thumbnail": "https://i.pinimg.com/originals/9b/1e/97/9b1e977d00b5d887608b156705a10759.png"};  
        return response;
    }
    else if (chain == 'arbitrum') {
        response = {"chain": "arbitrum",
                    "token_address": "0x0000000000000000000000000000000000000000",
                    "symbol": "ETH",
                    "name": "Ethereum",
                    "decimals": 18,
                    "balance": result.balance,
                    "logo": "https://w7.pngwing.com/pngs/268/1013/png-transparent-ethereum-eth-hd-logo-thumbnail.png",
                    "possible_spam": false,
                    "thumbnail": "https://w7.pngwing.com/pngs/268/1013/png-transparent-ethereum-eth-hd-logo-thumbnail.png"};  
        return response;
    }
    else if (chain == 'gnosis') {
        response = {"chain": "gnosis",
                    "token_address": "0x0000000000000000000000000000000000000000",
                    "symbol": "XDai",
                    "name": "xDai",
                    "decimals": 18,
                    "balance": result.balance,
                    "logo": "https://s2.coinmarketcap.com/static/img/coins/200x200/8635.png",
                    "possible_spam": false,
                    "thumbnail": "https://s2.coinmarketcap.com/static/img/coins/200x200/8635.png"};  
        return response;
    }
    return chain, result
}

export const prepareERC20Result = (chain, result) => {
    let response = [];
    for (let i = 0; i < result.length; i++) {
        result[i].chain = "eth";
        response.push(result[i]);
    }
    return response;
}

export const mergeBalances = (native_results, erc20_results) => {
    const merged_results = [];
    for (let i = 0; i < native_results.length; i++) {
        let itemERC20 = erc20_results[i];
        let itemNative = native_results[i];
        merged_results.push(itemNative);
        for (let j = 0; j < itemERC20.length; j++) {
            if (itemERC20[j].possible_spam == false){
                merged_results.push(itemERC20[j]);
            }
        }
    }
    return merged_results;
}