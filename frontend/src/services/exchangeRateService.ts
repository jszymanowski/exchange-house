import Big from "big.js";
import ProperDate from "@jszymanowski/proper-date.js";

import exchangeHouseClient, {
  handleError,
} from "@/integrations/exchangeHouseClient";
import { CurrencyPair, ExchangeRate } from "@/types";

interface CurrencyPairResponse {
  data: CurrencyPair[];
}

export const getAvailableCurrencyPairs =
  async (): Promise<CurrencyPairResponse> => {
    try {
      const response = await exchangeHouseClient.get<CurrencyPairResponse>(
        "exchange_rates/available_currency_pairs",
      );
      return response.data;
    } catch (error) {
      throw new Error(handleError(error));
    }
  };

interface LatestExchangeRateResponse extends CurrencyPair {
  data: ExchangeRate;
}

export const getLatestExchangeRate = async (
  baseCurrencyCode: string,
  quoteCurrencyCode: string,
): Promise<LatestExchangeRateResponse> => {
  try {
    const response = await exchangeHouseClient.get<LatestExchangeRateResponse>(
      `exchange_rates/${baseCurrencyCode}/${quoteCurrencyCode}/latest`,
    );
    return {
      baseCurrencyCode: response.data.baseCurrencyCode,
      quoteCurrencyCode: response.data.quoteCurrencyCode,
      data: {
        date: new ProperDate(response.data.data.date),
        rate: Big(response.data.data.rate),
      },
    };
  } catch (error) {
    throw new Error(handleError(error));
  }
};
