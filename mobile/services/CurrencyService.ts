import { Currency } from "@/models/Currency";
import { ExchangeRate } from "@/models/ExchangeRate";

export class CurrencyService {
  constructor(private readonly currency: Currency) {}

  static getSelectableCurrencies(): Currency[] {
    const allCurrencyCodes = ExchangeRate.getExchangeRates().map((rate) => rate.quoteCurrency.code);
    const currenciesWithExchangeRates = ExchangeRate.getQuoteCurrencyCodes("USD");

    const selectableCurrencies = allCurrencyCodes.filter((code) => currenciesWithExchangeRates.includes(code));
    return selectableCurrencies.map((code) => new Currency(code));
  }
}
