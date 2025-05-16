from datetime import date

from pydantic import BaseModel


class DateListResponse(BaseModel):
    data: list[date]
