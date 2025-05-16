export interface CurrencyMetadata {
  name: string
  symbol: string
  flag: string
  decimals: number
  lastUpdated?: FirebaseFirestore.Timestamp
}

export interface ExchangeRates {
  base: string
  rates: Record<string, number>
  date: string
  timestamp: FirebaseFirestore.Timestamp
}

export interface CurrenciesResponse {
  currencies: Record<string, CurrencyMetadata>
}
