import json

from app.models.currency_metadata import CurrencyMetadata


class CurrencyCollection:
    def __init__(self) -> None:
        self.initialized = False

    def initialize(self) -> None:
        with open("app/data/currencies.json") as f:
            data = json.load(f)
            currency_codes = list(data.keys())
            self.currencies = [
                CurrencyMetadata.from_dict(currency_code, data[currency_code]) for currency_code in currency_codes
            ]
            self.initialized = True

    def get_currencies(self) -> list[CurrencyMetadata]:
        if not self.initialized:
            self.initialize()
        return self.currencies


currencies_collection = CurrencyCollection()


class CurrenciesRepository:
    def get_currencies(self) -> list[CurrencyMetadata]:
        return currencies_collection.get_currencies()
