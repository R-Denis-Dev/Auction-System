from __future__ import annotations

import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine

from src.infrastructure.database.config import Base, engine
from src.infrastructure.database.models import user  # важно, чтобы модель импортировалась


async def init_models(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_models(engine))