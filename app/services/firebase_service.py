from app.core.firebase import db
from app.core.logger import get_logger
from app.models import Currency, ExchangeRate
from app.schema.exchange_rate_response import ExchangeRateData


class FirebaseExchangeRateData(ExchangeRateData):
    base_currency_code: Currency
    quote_currency_code: Currency

    @classmethod
    def from_model(cls, model: ExchangeRate) -> "FirebaseExchangeRateData":
        return cls(
            base_currency_code=model.base_currency_code,
            quote_currency_code=model.quote_currency_code,
            date=model.as_of,
            rate=model.rate,
        )


class FirebaseService:
    def __init__(self):
        self.db = db
        self.logger = get_logger("firebase")

    def update_exchange_rates(self, exchange_rates: list[ExchangeRate]):
        rates_ref = db.collection("exchangeRates").document("latest")

        # Prepare the data to write
        data = self._build_firebase_data(exchange_rates)

        # Write to Firestore
        try:
            rates_ref.set(data)
            sample_rate = data[0]
            self.logger.info(f"Updated exchange rates as of {sample_rate.date}")
        except Exception as e:
            self.logger.error(f"Error updating exchange rates: {e}")
            raise e

    def _build_firebase_data(self, exchange_rates: list[ExchangeRate]) -> list[FirebaseExchangeRateData]:
        return [FirebaseExchangeRateData.from_model(rate) for rate in exchange_rates]
