import type Big from "big.js";
import type ProperDate from "@jszymanowski/proper-date.js";

export type { CurrencyCode } from "@/currencies";

export type CurrencyPair = {
  baseCurrencyCode: string;
  quoteCurrencyCode: string;
};

export type ExchangeRate = {
  date: ProperDate;
  rate: Big;
};
