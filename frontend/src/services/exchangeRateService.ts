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


interface RawAvailableDatesResponse {
  data: string[];
}
interface AvailableDatesResponse {
  data: ProperDate[];
}

export const getAvailableDates =
  async (): Promise<AvailableDatesResponse> => {
    try {
      const response = await exchangeHouseClient.get<RawAvailableDatesResponse>(
        "exchange_rates/available_dates",
      );
      const data = response.data.data
        .map((item) => new ProperDate(item))
        .sort();
      return { data };
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

interface HistoricalExchangeRateResponse extends CurrencyPair {
  data: ExchangeRate[];
}

interface PaginatedHistoricalExchangeRateResponse
  extends HistoricalExchangeRateResponse {
  page: number;
  pages: number;
  total: number;
  size: number;
}

export const getHistoricalExchangeRates = async (
  baseCurrencyCode: string,
  quoteCurrencyCode: string,
  startDate?: ProperDate,
): Promise<HistoricalExchangeRateResponse> => {
  let page = 1;
  let totalPages = 1;
  const allData: ExchangeRate[] = [];

  while (page <= totalPages) {
    const response = await _getHistoricalExchangeRates(
      baseCurrencyCode,
      quoteCurrencyCode,
      startDate,
      page,
    );
    allData.push(...response.data);
    totalPages = response.pages;
    page++;
  }

  return {
    baseCurrencyCode,
    quoteCurrencyCode,
    data: allData,
  };
};

const _getHistoricalExchangeRates = async (
  baseCurrencyCode: string,
  quoteCurrencyCode: string,
  startDate?: ProperDate,
  page = 1,
): Promise<PaginatedHistoricalExchangeRateResponse> => {
  try {
    const { data: responseData } =
      await exchangeHouseClient.get<PaginatedHistoricalExchangeRateResponse>(
        `exchange_rates/${baseCurrencyCode}/${quoteCurrencyCode}/historical`,
        {
          params: {
            start_date: startDate?.toString(),
            page,
            order: "asc",
          },
        },
      );
    const data = responseData.data.map((item) => ({
      date: new ProperDate(item.date),
      rate: Big(item.rate),
    }));
    return {
      baseCurrencyCode: responseData.baseCurrencyCode,
      quoteCurrencyCode: responseData.quoteCurrencyCode,
      data,
      page: responseData.page,
      pages: responseData.pages,
      total: responseData.total,
      size: responseData.size,
    };
  } catch (error) {
    throw new Error(handleError(error));
  }
};
