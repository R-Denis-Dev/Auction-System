from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from src.domain.common.value_objects import BidId, LotId
from src.domain.auctions.entities import Bid


class IBidRepository(ABC):
    @abstractmethod
    async def get_by_id(self, bid_id: BidId) -> Bid | None: ...

    @abstractmethod
    async def list_for_lot(self, lot_id: LotId) -> Sequence[Bid]: ...

    @abstractmethod
    async def add(self, bid: Bid) -> Bid: ...