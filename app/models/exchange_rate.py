import uuid

from tortoise import fields
from tortoise.models import Model


class ExchangeRate(Model):
    """
    Model representing exchange rates between currency pairs.

    Stores historical exchange rate data with source information.
    """

    id: fields.UUIDField = fields.UUIDField(default=uuid.uuid4, primary_key=True)
    as_of: fields.DateField = fields.DateField(null=False)
    base_currency_code: fields.CharField = fields.CharField(max_length=3, null=False)
    quote_currency_code: fields.CharField = fields.CharField(max_length=3, null=False)
    rate: fields.DecimalField = fields.DecimalField(max_digits=18, decimal_places=8, null=False)
    data_source: fields.CharField = fields.CharField(max_length=20, null=False)
    created_at: fields.DatetimeField = fields.DatetimeField(
        auto_now=True,
        null=False,
    )
    updated_at: fields.DatetimeField = fields.DatetimeField(
        auto_now_add=True,
        null=False,
    )

    class Meta:
        table = "exchange_rates"
        indexes = (
            ("as_of", "base_currency_code", "quote_currency_code"),
            ("base_currency_code", "quote_currency_code"),
        )
        unique_together = ("as_of", "base_currency_code", "quote_currency_code")
