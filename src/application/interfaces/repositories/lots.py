from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence

from src.domain.common.value_objects import LotId, UserId
from src.domain.auctions.entities import Lot, AuctionStatus


class ILotRepository(ABC):
    @abstractmethod
    async def get_by_id(self, lot_id: LotId) -> Lot | None: ...

    @abstractmethod
    async def list_active(self, now: datetime) -> Sequence[Lot]: ...

    @abstractmethod
    async def list_by_owner(self, owner_id: UserId) -> Sequence[Lot]: ...

    @abstractmethod
    async def add(self, lot: Lot) -> Lot: ...

    @abstractmethod
    async def update(self, lot: Lot) -> Lot: ...

    @abstractmethod
    async def list_for_ending(self, now: datetime) -> Sequence[Lot]:...