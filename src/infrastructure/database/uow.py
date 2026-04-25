from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.unit_of_work import IUnitOFWork
from src.application.interfaces.repositories.users import IUserRepository
from src.infrastructure.database.repositories.users import UserRepository
from src.infrastructure.database.repositories.lots import LotRepository
from src.infrastructure.database.repositories.bids import BidRepository


class SqlAlchemyUnitOfWork(IUnitOFWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.users: IUserRepository = UserRepository(session)
        self.lots = LotRepository(session)
        self.bids = BidRepository(session)

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()