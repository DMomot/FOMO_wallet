import axios from 'axios';
import { prepareNativeResult, prepareERC20Result } from '../helpers/prepareResultsMoralis.js';

const apiClient = axios.create({
  baseURL: 'https://deep-index.moralis.io/api/v2.2/', // 
  withCredentials: false,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-API-Key': process.env.VUE_APP_API_URL
  }
});

export const getNativeBalancesByChain = async (chain, walletAddress) => {
  try {
      const response = await apiClient.get(walletAddress + '/balance/?chain=' + chain);
      const resultNative = prepareNativeResult(chain, response.data);
      return resultNative;
  } catch (error) {
      throw new Error(`[RWV] ApiService ${error}`);
  }
}

export const getERC20BalancesByChain = async (chain, walletAddress) => {
    try {
        const response = await apiClient.get(walletAddress + '/erc20/?chain=' + chain);
        const resultERC20 = prepareERC20Result(chain, response.data);
        return resultERC20;
    } catch (error) {
        throw new Error(`[RWV] ApiService ${error}`);
    }
  }