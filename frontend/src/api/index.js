import axios from 'axios';
import { prepareNativeResult, prepareERC20Result } from '../helpers/prepareResultsMoralis.js';

const apiClient = axios.create({
  baseURL: 'https://deep-index.moralis.io/api/v2.2/', // 
  withCredentials: false,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-API-Key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6Ijk0NTJjYTQ4LWQ0MjUtNGU1MC04ZmU5LTc5Y2E1Y2U5MzQxNSIsIm9yZ0lkIjoiMjc1OTYwIiwidXNlcklkIjoiMjgxNDM1IiwidHlwZUlkIjoiYjAxYTcwZjYtM2RjNy00MGZhLWFiYWItZTk0NTVlNjE4YWYzIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE2ODg4MTI2MTMsImV4cCI6NDg0NDU3MjYxM30.fp7-zUy5bp8AqO1imKM6Yl7f2qJ7ji1ZCZ0r9ELfC6E'
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