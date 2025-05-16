import { CURRENCIES, type CurrencyCode } from "@/data/currencies";

export class Currency {
  code: CurrencyCode;
  name: string;
  symbol: string;
  flag: string;
  decimalPlaces: number;

  constructor(iso_code: CurrencyCode) {
    const metadata = CURRENCIES[iso_code];
    this.code = iso_code;
    this.name = metadata.name;
    this.symbol = metadata.symbol;
    this.flag = metadata.flag;
    if (metadata.decimalPlaces != null && metadata.decimalPlaces !== undefined) {
      this.decimalPlaces = metadata.decimalPlaces;
    } else {
      this.decimalPlaces = 2;
    }
  }

  static getCurrencies(): Currency[] {
    return Object.keys(CURRENCIES).map((code) => new Currency(code));
  }

  static getCurrency(code: CurrencyCode): Currency | null {
    const metadata = CURRENCIES[code];
    if (!metadata) {
      return null;
    }
    return new Currency(code);
  }
}
