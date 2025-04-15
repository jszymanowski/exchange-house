from datetime import date

from pydantic_core import PydanticCustomError, core_schema


class AvailableDate(date):
    """A date in the past or today."""

    @classmethod
    def __get_pydantic_core_schema__(cls, _source, handler):  # type: ignore
        return core_schema.no_info_after_validator_function(cls.validate, handler(date))

    @classmethod
    def validate(cls, value: date) -> date:
        if not isinstance(value, date):
            raise TypeError("Expected a date")

        if value > date.today():
            raise PydanticCustomError("date_not_in_past_or_today", "Date must be in the past or today")

        return value
