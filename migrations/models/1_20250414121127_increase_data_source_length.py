from tortoise import BaseDBAsyncClient


async def upgrade(_db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "exchange_rates" ALTER COLUMN "data_source" TYPE VARCHAR(50) USING "data_source"::VARCHAR(50);"""


async def downgrade(_db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "exchange_rates" ALTER COLUMN "data_source" TYPE VARCHAR(20) USING "data_source"::VARCHAR(20);"""
