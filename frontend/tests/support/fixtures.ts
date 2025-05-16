import ProperDate from "@still-forest/proper-date.js";
import Big from "big.js";
import type { CurrencyPair, ExchangeRate } from "@/types";

export const createCurrencyPair = (overrides: Partial<CurrencyPair> = {}): CurrencyPair => ({
  baseCurrencyCode: "USD",
  quoteCurrencyCode: "EUR",
  ...overrides,
});

export const createExchangeRate = (overrides?: Partial<ExchangeRate>): ExchangeRate => ({
  date: new ProperDate("2024-12-25"),
  rate: Big("1.123"),
  ...overrides,
});
