from datetime import datetime
from typing import TypedDict

from firebase_admin.firestore import Client

from app.core.config import firebase_settings
from app.core.firebase import get_firebase_client
from app.core.logger import get_logger
from app.models import Currency, ExchangeRate
from app.models.currency_metadata import CurrencyMetadata, CurrencyMetadataDict
from app.services.currency_service import get_currency_service
from app.utils import quantize_decimal


class FirebaseCurrenciesData(TypedDict):
    data: dict[str, CurrencyMetadataDict]
    timestamp: str


class FirebaseCurrenciesDataBuilder:
    @classmethod
    def from_model_list(cls, model_list: list[CurrencyMetadata]) -> "FirebaseCurrenciesData":
        data = {}
        for model in model_list:
            data[model.iso_code] = model.to_dict()

        return FirebaseCurrenciesData(
            data=data,
            timestamp=str(datetime.now()),
        )


class FirebaseExchangeRateData(TypedDict):
    base: str
    rates: dict[str, str]
    date: str
    timestamp: str


class FirebaseExchangeRateDataBuilder:
    @classmethod
    def from_model_list(cls, model_list: list[ExchangeRate]) -> "FirebaseExchangeRateData":
        rates = {}
        for model in model_list:
            rates[model.quote_currency_code] = str(quantize_decimal(model.rate))

        return FirebaseExchangeRateData(
            base=Currency(firebase_settings.base_currency_code),
            rates=rates,
            date=str(model_list[0].as_of),
            timestamp=str(datetime.now()),
        )


class FirebaseService:
    def __init__(self, client: Client | None = None):
        self.client = client or get_firebase_client()
        self.currencies_repository = get_currency_service()
        self.logger = get_logger("firebase")

    def update_currencies(self) -> tuple[bool, Exception | None]:
        currencies_metadata = self.currencies_repository.get_all_currencies()

        if len(currencies_metadata) == 0:
            raise ValueError("No currencies metadata found")

        currencies_ref = self.client.collection("currencies").document("metadata")
        data = FirebaseCurrenciesDataBuilder.from_model_list(currencies_metadata)

        try:
            currencies_ref.set(data)
            self.logger.info("Updated currencies")
            return True, None
        except Exception as e:
            self.logger.error(f"Error updating currencies: {e}")
            return False, e

    def update_exchange_rates(self, exchange_rates: list[ExchangeRate]) -> tuple[bool, Exception | None]:
        try:
            self._validate_exchange_rates(exchange_rates)
        except ValueError as e:
            self.logger.error(f"Invalid set of exchange rates: {e}")
            raise e

        rates_ref = self.client.collection("exchangeRates").document("latest")
        data = FirebaseExchangeRateDataBuilder.from_model_list(exchange_rates)

        try:
            rates_ref.set(data)
            self.logger.info(f"Updated exchange rates as of {data['date']}")
            return True, None
        except Exception as e:
            self.logger.error(f"Error updating exchange rates: {e}")
            return False, e

    def _validate_exchange_rates(self, exchange_rates: list[ExchangeRate]) -> None:
        if len(exchange_rates) == 0:
            raise ValueError("No exchange rates provided")

        as_of = exchange_rates[0].as_of

        for rate in exchange_rates:
            if rate.base_currency_code != Currency(firebase_settings.base_currency_code):
                raise ValueError(
                    f"Base currency code ({rate.base_currency_code}) differs from "
                    f"configuration ({firebase_settings.base_currency_code})"
                )

            if rate.as_of != as_of:
                raise ValueError(f"As of date ({rate.as_of}) differs from the first rate's as of date ({as_of})")
