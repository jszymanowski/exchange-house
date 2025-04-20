import exchangeHouseClient, {
  handleError,
} from "@/integrations/exchangeHouseClient";
import { CurrencyPair } from "@/types";

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
