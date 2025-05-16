import ProperDate from "@still-forest/proper-date.js";
import { Big } from "big.js";
import type { CurrencyCode } from "@/data/currencies";
import EXCHANGE_RATE_DATA from "@/data/exchange_rates.json";
import { parseTextAsNumber } from "@/utilities/number";
import { Currency } from "./Currency";

export class ExchangeRate {
  baseCurrency: Currency;
  quoteCurrency: Currency;
  rate: Big;
  date: ProperDate;

  constructor(
    baseCurrencyCode: CurrencyCode,
    quoteCurrencyCode: CurrencyCode,
    rate: string | number | Big,
    date: string | ProperDate,
  ) {
    this.baseCurrency = new Currency(baseCurrencyCode);
    this.quoteCurrency = new Currency(quoteCurrencyCode);
    this.rate = Big(rate);
    this.date = new ProperDate(date);
  }

  static getExchangeRates(): ExchangeRate[] {
    return EXCHANGE_RATE_DATA.exchangeRates.map(
      (rate) => new ExchangeRate(rate.baseCurrencyCode, rate.quoteCurrencyCode, rate.rate, rate.date),
    );
  }

  static getExchangeRate(baseCurrencyCode: CurrencyCode, quoteCurrencyCode: CurrencyCode): ExchangeRate | null {
    const rate = ExchangeRate.getExchangeRates().find(
      (rate) => rate.baseCurrency.code === baseCurrencyCode && rate.quoteCurrency.code === quoteCurrencyCode,
    );
    if (!rate) {
      return null;
    }
    return new ExchangeRate(rate.baseCurrency.code, rate.quoteCurrency.code, rate.rate, rate.date);
  }

  static getQuoteCurrencyCodes(baseCurrencyCode: CurrencyCode): CurrencyCode[] {
    const currencyCodes = EXCHANGE_RATE_DATA.exchangeRates
      .filter((rate) => rate.baseCurrencyCode === baseCurrencyCode)
      .map((rate) => rate.quoteCurrencyCode);
    return currencyCodes;
  }

  get formattedRate(): string {
    return parseTextAsNumber(this.rate.toFixed(this.quoteCurrency.decimalPlaces)).formatted;
  }

  get formattedDate(): string {
    return this.date.formatted;
  }
}
