from functools import partial

from tortoise.contrib.fastapi import RegisterTortoise

from app.core.config import settings

register_orm = partial(
    RegisterTortoise,
    db_url=settings.DATABASE_URL,
    modules={"models": ["app.models"]},
    generate_schemas=True,
)
