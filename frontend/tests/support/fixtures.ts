import { CurrencyPair } from "@/types";

export const createCurrencyPair = (
  overrides: Partial<CurrencyPair> = {},
): CurrencyPair => ({
  baseCurrencyCode: "USD",
  quoteCurrencyCode: "EUR",
  ...overrides,
});
