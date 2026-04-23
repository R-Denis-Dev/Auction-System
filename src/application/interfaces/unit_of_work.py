from __future__ import annotations

from abc import ABC , abstractmethod

from src.application.interfaces.repositories.users import IUserRepository


class IUnitOFWork(ABC):
    users:IUserRepository

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    @abstractmethod
    async def commit(self) -> None: ...
    @abstractmethod
    async def rollback(self) -> None: ...