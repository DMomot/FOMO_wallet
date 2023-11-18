export const prepareNativeResult = (chain, result) => {
    let response = {};
    if (chain == 'eth') {
        response.eth = {"token_address": "0x0000000000000000000000000000000000000000",
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
        response.polygon = {"token_address": "0x0000000000000000000000000000000000001010",
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
        response.arbitrum = {"token_address": "0x0000000000000000000000000000000000000000",
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
        response.gnosis = {"token_address": "0x0000000000000000000000000000000000000000",
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
    let response = {};
    if (chain == 'eth') {
        response.eth = result;
        return response;
    }
    else if (chain == 'polygon') {
        response.polygon = result;
        return response;
    }
    else if (chain == 'arbitrum') {
        response.arbitrum = result;
        return response;
    }
    else if (chain == 'gnosis') {
        response.gnosis = result;
        return response;
    }
    return chain, result
}

export const mergeBalances = (native_results, erc20_results) => {
    const merged_results = {};
    const chainIds = ['eth', 'polygon', 'arbitrum', 'gnosis'];
    for (let i = 0; i < erc20_results.length; i++) {
        let itemERC20 = erc20_results[i];
        let itemNative = native_results[i];
        merged_results[chainIds[i]] = itemERC20[chainIds[i]]
        merged_results[chainIds[i]].push(itemNative[chainIds[i]])
    }
    return merged_results;
}