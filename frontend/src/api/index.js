import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://fomogotchi.duckdns.org/api/fomo/', // 
  withCredentials: false,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
});

export const getFomoVibe = async (walletAddress) => {
  try {
      const response = await apiClient.get(walletAddress);
      return response.data;
  } catch (error) {
      throw new Error(`[RWV] ApiService ${error}`);
  }
}