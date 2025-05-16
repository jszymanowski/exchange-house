from typing import TypedDict

from pydantic import BaseModel

DEFAULT_DECIMALS = 2


class CurrencyMetadataDict(TypedDict):
    name: str
    symbol: str
    flag: str
    decimals: int | None


class CurrencyMetadata(BaseModel):
    name: str
    iso_code: str
    symbol: str
    flag: str
    decimals: int | None

    @classmethod
    def from_dict(cls, iso_code: str, data: CurrencyMetadataDict) -> "CurrencyMetadata":
        return cls(
            iso_code=iso_code,
            name=data["name"],
            symbol=data["symbol"],
            flag=data["flag"],
            decimals=data.get("decimals", DEFAULT_DECIMALS),
        )

    def to_dict(self) -> CurrencyMetadataDict:
        return {
            "name": self.name,
            "symbol": self.symbol,
            "flag": self.flag,
            "decimals": self.decimals,
        }
