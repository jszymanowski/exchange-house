from unittest.mock import MagicMock

import pytest

from app.models.currency_metadata import CurrencyMetadata
from app.services.currency_service import CurrencyService


@pytest.fixture
def mock_currencies_repository() -> MagicMock:
    mock_currencies_repository = MagicMock()
    mock_currencies_repository.get_currencies.return_value = [
        CurrencyMetadata(iso_code="USD", name="US Dollar", symbol="$", flag="🇺🇸", decimals=2),
        CurrencyMetadata(iso_code="EUR", name="Euro", symbol="€", flag="🇪🇺", decimals=2),
        CurrencyMetadata(iso_code="KRW", name="Korean Won", symbol="₩", flag="🇰🇷", decimals=0),
    ]
    return mock_currencies_repository


@pytest.mark.asyncio
async def test_get_all_currencies(mock_currencies_repository: MagicMock) -> None:
    currency_service = CurrencyService(mock_currencies_repository)

    results = currency_service.get_all_currencies()

    assert results == [
        CurrencyMetadata(iso_code="USD", name="US Dollar", symbol="$", flag="🇺🇸", decimals=2),
        CurrencyMetadata(iso_code="EUR", name="Euro", symbol="€", flag="🇪🇺", decimals=2),
        CurrencyMetadata(iso_code="KRW", name="Korean Won", symbol="₩", flag="🇰🇷", decimals=0),
    ]
