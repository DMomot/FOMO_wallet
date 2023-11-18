import { getNativeBalancesByChain, getERC20BalancesByChain }  from "@/api/index.js";
import { mergeBalances } from "@/helpers/prepareResultsMoralis.js";

export const getAllBalances = async (walletAddress) =>{
    const chainIds = ['eth', 'polygon', 'arbitrum', 'gnosis'];

    try {
        const native_results = await Promise.all(chainIds.map(chain_id => getNativeBalancesByChain(chain_id, walletAddress)));
        const erc20_results = await Promise.all(chainIds.map(chain_id => getERC20BalancesByChain(chain_id, walletAddress)));

        console.log('native_results', native_results)
        console.log('erc20_results', erc20_results)
        
        const merged_results = mergeBalances(native_results, erc20_results);

        return merged_results;
    } catch (error) {
        console.error('Произошла ошибка:', error);
        return [null, null];
    }
}






