from typing import TypeVar

from tortoise.models import Model

T = TypeVar("T", bound=Model)


class DatabaseTestHelper:
    @staticmethod
    async def count_records(model_class: type[T]) -> int:
        return await model_class.all().count()

    @staticmethod
    async def clear_table(model_class: type[T]) -> None:
        await model_class.all().delete()


def get_database_test_helper() -> DatabaseTestHelper:
    return DatabaseTestHelper()
