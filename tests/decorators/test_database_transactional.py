import pytest
from tortoise.exceptions import OperationalError

# Import your models and the transactional decorator
from app.decorators import database_transactional
from app.models import Currency, ExchangeRate
from tests.support.database_test_helper import DatabaseTestHelper
from tests.support.factories import build_exchange_rate


@database_transactional
async def create_test_object(base_currency_code: Currency, should_fail=False, db_connection=None):
    # Test function that uses the transactional decorator
    obj = build_exchange_rate(base_currency_code=base_currency_code, quote_currency_code="USD")
    await obj.save(using_db=db_connection)

    if should_fail:
        # Simulate a failure
        raise OperationalError("Simulated failure")

    return obj


@pytest.mark.asyncio
async def test_transactional_success(test_database: DatabaseTestHelper) -> None:
    # Test successful transaction
    obj = await create_test_object("EUR")

    # Verify object was created and committed
    assert await test_database.count_records(ExchangeRate) == 1
    assert obj.base_currency_code == "EUR"
    assert obj.quote_currency_code == "USD"


@pytest.mark.asyncio
async def test_transactional_rollback(test_database: DatabaseTestHelper) -> None:
    # Test transaction rollback on failure
    with pytest.raises(OperationalError):
        await create_test_object("EUR", should_fail=True)

    # Verify object was not committed
    assert await test_database.count_records(ExchangeRate) == 0


@pytest.mark.asyncio
async def test_nested_transactions(test_database: DatabaseTestHelper) -> None:
    # Test nested transactions (parent transaction controls commit/rollback)
    @database_transactional
    async def parent_function(db_connection=None):
        # Create object in parent transaction
        parent_obj = build_exchange_rate(base_currency_code="EUR")
        await parent_obj.save(using_db=db_connection)

        # Call child function with the same db_connection
        child_obj = await create_test_object("JPY", db_connection=db_connection)

        return parent_obj, child_obj

    # Run the test
    parent_obj, child_obj = await parent_function()

    # Verify both objects were created
    assert await test_database.count_records(ExchangeRate) == 2


@pytest.mark.asyncio
async def test_nested_transaction_rollback(test_database: DatabaseTestHelper) -> None:
    # Test rollback of parent transaction affects child transactions
    @database_transactional
    async def parent_with_rollback(db_connection=None):
        # Create object in parent transaction
        parent_obj = build_exchange_rate(base_currency_code="EUR")
        await parent_obj.save(using_db=db_connection)

        # Call child function with the same db_connection
        await create_test_object("JPY", db_connection=db_connection)

        # Simulate failure in parent
        raise OperationalError("Parent failed")

    # Run the test
    with pytest.raises(OperationalError):
        await parent_with_rollback()

    # Verify neither object was committed
    assert await test_database.count_records(ExchangeRate) == 0
