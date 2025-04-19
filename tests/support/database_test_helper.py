from tortoise.models import Model


class DatabaseTestHelper:
    @staticmethod
    async def count_records(model_class: Model) -> int:
        return await model_class.all().count()

    @staticmethod
    async def clear_table(model_class: Model) -> None:
        await model_class.all().delete()
