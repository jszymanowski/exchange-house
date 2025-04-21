import { CurrencyPair, ExchangeRate } from "@/types";
import ProperDate from "@jszymanowski/proper-date.js";
import Big from "big.js";

export const createCurrencyPair = (
  overrides: Partial<CurrencyPair> = {},
): CurrencyPair => ({
  baseCurrencyCode: "USD",
  quoteCurrencyCode: "EUR",
  ...overrides,
});

export const createExchangeRate = (
  overrides?: Partial<ExchangeRate>,
): ExchangeRate => ({
  date: new ProperDate("2024-12-25"),
  rate: Big("1.123"),
  ...overrides,
});
