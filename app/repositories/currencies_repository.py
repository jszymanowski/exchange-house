import json

from app.models.currency_metadata import CurrencyMetadata


class CurrencyCollection:
    def __init__(self) -> None:
        self.initialized = False

    def initialize(self) -> None:
        try:
            with open("app/data/currencies.json") as f:
                data = json.load(f)
                currency_codes = list(data.keys())
                self.currencies = [
                    CurrencyMetadata.from_dict(currency_code, data[currency_code]) for currency_code in currency_codes
                ]
                self.initialized = True
        except FileNotFoundError as e:
            raise ValueError("Currency data file not found: app/data/currencies.json") from e
        except json.JSONDecodeError as e:
            raise ValueError("Currency data file contains invalid JSON") from e
        except Exception as e:
            raise ValueError(f"Failed to load currency data: {str(e)}") from e

    def get_currencies(self) -> list[CurrencyMetadata]:
        if not self.initialized:
            self.initialize()
        return self.currencies


currencies_collection = CurrencyCollection()


class CurrenciesRepository:
    def get_currencies(self) -> list[CurrencyMetadata]:
        return currencies_collection.get_currencies()
