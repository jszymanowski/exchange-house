from typing import Any

from pydantic_extra_types.currency_code import Currency as BaseCurrency


class Currency(BaseCurrency):
    def is_valid(self) -> bool:
        return self.iso_code in BaseCurrency.allowed_currencies

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Currency):
            return self.iso_code == other.iso_code

        elif isinstance(other, BaseCurrency):
            return self.iso_code == other.upper()

        elif isinstance(other, str):
            return self.iso_code == other.upper()

        return NotImplemented

    @property
    def iso_code(self) -> str:
        return self.upper()
