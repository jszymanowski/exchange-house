import pytest

from app.models.currency_metadata import CurrencyMetadata
from app.repositories.currencies_repository import CurrenciesRepository

EXPECTED_CURRENCY_CODES = [
    "AED",
    "AFN",
    "ALL",
    "AMD",
    "ANG",
    "AOA",
    "ARS",
    "AUD",
    "AWG",
    "AZN",
    "BAM",
    "BBD",
    "BDT",
    "BGN",
    "BHD",
    "BIF",
    "BMD",
    "BND",
    "BOB",
    "BRL",
    "BSD",
    "BTN",
    "BWP",
    "BYN",
    "BZD",
    "CAD",
    "CDF",
    "CHF",
    "CLP",
    "CNY",
    "COP",
    "CRC",
    "CUP",
    "CVE",
    "CZK",
    "DJF",
    "DKK",
    "DOP",
    "DZD",
    "EGP",
    "ERN",
    "ETB",
    "EUR",
    "FJD",
    "FKP",
    "GBP",
    "GEL",
    "GHS",
    "GIP",
    "GMD",
    "GNF",
    "GTQ",
    "GYD",
    "HKD",
    "HNL",
    "HRK",
    "HTG",
    "HUF",
    "IDR",
    "ILS",
    "INR",
    "IQD",
    "IRR",
    "ISK",
    "JMD",
    "JOD",
    "JPY",
    "KES",
    "KGS",
    "KHR",
    "KMF",
    "KPW",
    "KRW",
    "KWD",
    "KYD",
    "KZT",
    "LAK",
    "LBP",
    "LKR",
    "LRD",
    "LSL",
    "LYD",
    "MAD",
    "MDL",
    "MGA",
    "MKD",
    "MMK",
    "MNT",
    "MOP",
    "MRU",
    "MUR",
    "MVR",
    "MWK",
    "MXN",
    "MYR",
    "MZN",
    "NAD",
    "NGN",
    "NIO",
    "NOK",
    "NPR",
    "NZD",
    "OMR",
    "PAB",
    "PEN",
    "PGK",
    "PHP",
    "PKR",
    "PLN",
    "PYG",
    "QAR",
    "RON",
    "RSD",
    "RUB",
    "RWF",
    "SAR",
    "SBD",
    "SCR",
    "SDG",
    "SEK",
    "SGD",
    "SHP",
    "SLE",
    "SOS",
    "SRD",
    "SSP",
    "STN",
    "SYP",
    "SZL",
    "THB",
    "TJS",
    "TMT",
    "TND",
    "TOP",
    "TRY",
    "TTD",
    "TWD",
    "TZS",
    "UAH",
    "UGX",
    "USD",
    "UYU",
    "UZS",
    "VES",
    "VND",
    "VUV",
    "WST",
    "XAF",
    "XCD",
    "XOF",
    "XPF",
    "YER",
    "ZAR",
    "ZMW",
    "ZWL",
]


@pytest.mark.asyncio
async def test_get_all_currencies() -> None:
    repository = CurrenciesRepository()
    result = repository.get_currencies()

    # assert len(result) == len(EXPECTED_CURRENCY_CODES)
    currency_codes = [c.iso_code for c in result]
    assert currency_codes == EXPECTED_CURRENCY_CODES

    krw = next(filter(lambda c: c.iso_code == "KRW", result))
    assert isinstance(krw, CurrencyMetadata)
    assert krw.iso_code == "KRW"
    assert krw.name == "South Korean Won"
    assert krw.symbol == "₩"
    assert krw.flag == "🇰🇷"
    assert krw.decimals == 0

    usd = next(filter(lambda c: c.iso_code == "USD", result))
    assert isinstance(usd, CurrencyMetadata)
    assert usd.iso_code == "USD"
    assert usd.name == "United States Dollar"
    assert usd.symbol == "$"
    assert usd.flag == "🇺🇲"
    assert usd.decimals == 2

    eur = next(filter(lambda c: c.iso_code == "EUR", result))
    assert isinstance(eur, CurrencyMetadata)
    assert eur.iso_code == "EUR"
    assert eur.name == "Euro"
    assert eur.symbol == "€"
    assert eur.flag == "🇪🇺"
    assert eur.decimals == 2

    myr = next(filter(lambda c: c.iso_code == "MYR", result))
    assert isinstance(myr, CurrencyMetadata)
    assert myr.iso_code == "MYR"
    assert myr.name == "Malaysian Ringgit"
    assert myr.symbol == "RM"
    assert myr.flag == "🇲🇾"
    assert myr.decimals == 2
