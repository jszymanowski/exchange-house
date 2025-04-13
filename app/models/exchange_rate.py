import uuid
from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class ExchangeRate(Model):
    id: fields.UUIDField = fields.UUIDField(default=uuid.uuid4, pk=True)
    as_of: fields.DateField = fields.DateField(null=False)
    base_currency: fields.CharField = fields.CharField(max_length=3, null=False)
    quote_currency: fields.CharField = fields.CharField(max_length=3, null=False)
    rate: fields.DecimalField = fields.DecimalField(
        max_digits=18, decimal_places=8, null=False
    )
    source: fields.CharField = fields.CharField(max_length=20, null=False)
    created_at: fields.DatetimeField = fields.DatetimeField(
        default=datetime.now(datetime.UTC),  # type: ignore # Python 3.11+ feature
        null=False,
    )
    updated_at: fields.DatetimeField = fields.DatetimeField(
        default=datetime.now(datetime.UTC),  # type: ignore # Python 3.11+ feature
        null=False,
    )
