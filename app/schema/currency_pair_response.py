from pydantic import BaseModel


class CurrencyPairResponse(BaseModel):
    from_iso_code: str
    to_iso_code: str
