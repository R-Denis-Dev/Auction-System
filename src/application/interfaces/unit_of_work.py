from __future__ import annotations

from abc import ABC , abstractmethod

from src.application.interfaces.repositories.users import IUserRepository
from src.application.interfaces.repositories.lots import ILotRepository
from src.application.interfaces.repositories.bids import IBidRepository


class IUnitOFWork(ABC):
    users: IUserRepository
    lots: ILotRepository
    bids: IBidRepository

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