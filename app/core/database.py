from functools import partial

from tortoise.contrib.fastapi import RegisterTortoise

from app.core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.database_url},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

register_orm = partial(
    RegisterTortoise,
    config=TORTOISE_ORM,
)
