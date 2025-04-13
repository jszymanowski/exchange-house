from tortoise import BaseDBAsyncClient


async def upgrade(_db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "exchange_rates" (
    "id" UUID NOT NULL PRIMARY KEY,
    "as_of" DATE NOT NULL,
    "base_currency_code" VARCHAR(3) NOT NULL,
    "quote_currency_code" VARCHAR(3) NOT NULL,
    "rate" DECIMAL(18,8) NOT NULL,
    "data_source" VARCHAR(20) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "uid_exchange_ra_as_of_7db101" UNIQUE ("as_of", "base_currency_code", "quote_currency_code")
);
CREATE INDEX IF NOT EXISTS "idx_exchange_ra_as_of_7db101" ON "exchange_rates" ("as_of", "base_currency_code", "quote_currency_code");
CREATE INDEX IF NOT EXISTS "idx_exchange_ra_base_cu_0b5c51" ON "exchange_rates" ("base_currency_code", "quote_currency_code");
COMMENT ON TABLE "exchange_rates" IS 'Model representing exchange rates between currency pairs.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(_db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "exchange_rates";
        DROP TABLE IF EXISTS "aerich";
        """
