class DatabaseTestHelper:
    @staticmethod
    async def count_records(model_class):
        return await model_class.all().count()

    @staticmethod
    async def clear_table(model_class):
        await model_class.all().delete()
