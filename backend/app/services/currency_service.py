from app.models.currency_metadata import CurrencyMetadata
from app.repositories.currencies_repository import CurrenciesRepository


class CurrencyService:
    def __init__(self, currencies_repository: CurrenciesRepository):
        self.currencies_repository = currencies_repository

    def get_all_currencies(self) -> list[CurrencyMetadata]:
        return self.currencies_repository.get_currencies()


def get_currency_service() -> CurrencyService:
    return CurrencyService(currencies_repository=CurrenciesRepository())
