from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.unit_of_work import IUnitOFWork
from src.application.interfaces.repositories.users import IUserRepository
from src.infrastructure.database.repositories.users import UserRepository



class SqlAlchemyUnitOfWork(IUnitOFWork):
    def __init__(self, session:AsyncSession) -> None:
        self._session = session
        self.users:IUserRepository = UserRepository(session)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self):
        return self._session.rollback()
    


