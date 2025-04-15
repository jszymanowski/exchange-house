import pytest
from pydantic_extra_types.currency_code import Currency as BaseCurrency

from app.models.currency import Currency


class TestCurrency:
    @pytest.mark.parametrize("currency_code", ["USD", "JPY"])
    def test_is_valid(self, currency_code: str):
        assert Currency(currency_code).is_valid()

    @pytest.mark.parametrize("currency_code", ["BTC", "XXX"])
    def test_is_invalid(self, currency_code: str):
        assert not Currency(currency_code).is_valid()

    @pytest.mark.parametrize("currency_code", ["USD", "JPY", "usd", "uSd", "BTC", "xxx"])
    def test_iso_code(self, currency_code: str):
        assert Currency(currency_code).iso_code == currency_code.upper()

    @pytest.mark.parametrize("currency_code", ["USD", "usd", "Usd", "USd"])
    def test_equality(self, currency_code: str):
        assert Currency(currency_code) == Currency("USD")
        assert Currency("USD") == BaseCurrency(currency_code)
        assert Currency(currency_code) == "USD"
        assert Currency(currency_code) == "usd"
        assert Currency(currency_code) == "usD"
        assert Currency(currency_code) == "USd"
        assert BaseCurrency(currency_code) == Currency("USD")

        # Pydantic Currency (BaseCurrency) and Currency equality methods are not overridden
        if currency_code == "USD":
            assert currency_code == Currency("USD")
            assert currency_code == BaseCurrency("USD")
            assert BaseCurrency(currency_code) == "USD"
            assert BaseCurrency(currency_code) == Currency("USD")
        else:
            assert currency_code != Currency("USD")
            assert currency_code != BaseCurrency("USD")
            assert BaseCurrency(currency_code) != "USD"
            assert BaseCurrency(currency_code) != Currency("USD")

    @pytest.mark.parametrize("currency_code", ["USD", "JPZ", "BTC"])
    def test_inequality(self, currency_code: str):
        assert Currency(currency_code) != Currency("JPY")
        assert BaseCurrency(currency_code) != Currency("JPY")
        assert currency_code != Currency("JPY")
