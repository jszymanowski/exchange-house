import axios from "axios";

import { API_URL } from "@/config";
import { CurrencyPair } from "@/types";

type Primitive = string | number | boolean | null | undefined;

type CamelCaseKeys<T> = T extends Primitive
  ? T
  : T extends Array<infer U>
    ? Array<CamelCaseKeys<U>>
    : {
        [K in keyof T as K extends string
          ? `${Uncapitalize<K extends `${infer F}_${infer R}` ? `${F}${Capitalize<R>}` : K>}`
          : never]: CamelCaseKeys<T[K]>;
      };

function toCamelCase(snakeStr: string): string {
  return snakeStr.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

function toCamelCaseKeys<T>(obj: T): CamelCaseKeys<T> {
  if (Array.isArray(obj)) {
    return obj.map((item) => toCamelCaseKeys(item)) as CamelCaseKeys<T>;
  } else if (obj && typeof obj === "object") {
    return Object.keys(obj).reduce(
      (acc, key) => {
        const camelKey = toCamelCase(key);
        (acc as Record<string, unknown>)[camelKey] = toCamelCaseKeys((obj as Record<string, unknown>)[key]);
        return acc;
      },
      {} as CamelCaseKeys<T>,
    );
  }
  return obj as CamelCaseKeys<T>;
}

const axiosInstance = axios.create({
  baseURL: `${API_URL}/api/v1/`,
  timeout: import.meta.env.VITE_API_TIMEOUT ? Number.parseInt(import.meta.env.VITE_API_TIMEOUT) : 10_000,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosInstance.interceptors.response.use(
  (response) => {
    response.data = toCamelCaseKeys(response.data);
    return response;
  },
  (error) => {
  const sanitizedError = {
    message: error.response?.data?.message || error.message || "An unexpected error occurred",
    status: error.response?.status || 500
  };
  return Promise.reject(sanitizedError);
  },
);

const handleError = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    return error.response?.data?.message || "An unexpected error occurred";
  } else if (error instanceof Error) {
    return error.message;
  }
  return "An unexpected error occurred";
};

interface CurrencyPairResponse {
  data: CurrencyPair[];
}

export const getAvailableCurrencyPairs = async (): Promise<CurrencyPairResponse> => {
  try {
    const response = await axiosInstance.get<CurrencyPairResponse>(
      "exchange_rates/available_currency_pairs",
    );
    return response.data;
  } catch (error) {
    throw new Error(handleError(error));
  }
};

export default axiosInstance;
