import axios from "axios";

import { API_URL } from "@/config";
import { CurrencyPair } from "@/types";

const axiosInstance = axios.create({
  baseURL: `${API_URL}/api/v1`,
  timeout: 15_000,
  headers: {
    "Content-Type": "application/json",
  },
});

const handleError = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    return error.response?.data?.message || "An unexpected error occurred";
  } else if (error instanceof Error) {
    return error.message;
  }
  return "An unexpected error occurred";
};

export const getAvailableCurrencyPairs = async (): Promise<CurrencyPair[]> => {
  try {
    const response = await axiosInstance.get<CurrencyPair[]>(
      "/v1/exchange_rates/available_currency_pairs",
    );
    return response.data;
  } catch (error) {
    throw new Error(handleError(error));
  }
};

export default axiosInstance;
