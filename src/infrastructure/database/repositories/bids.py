from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories.bids import IBidRepository
from src.domain.auctions.entities import Bid
from src.domain.common.value_objects import BidId, LotId, UserId
from src.infrastructure.database.models.bid import BidModel


class BidRepository(IBidRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, bid_id: BidId) -> Bid | None:
        stmt = select(BidModel).where(BidModel.id == int(bid_id.value))
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def list_for_lot(self, lot_id: LotId) -> Sequence[Bid]:
        stmt = select(BidModel).where(BidModel.lot_id == int(lot_id.value))
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    async def add(self, bid: Bid) -> Bid:
        model = BidModel(
            lot_id=int(bid.lot_id.value),
            user_id=int(bid.user_id.value),
            amount=bid.amount,
            created_at=bid.created_at,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: BidModel) -> Bid:
        return Bid(
            id=BidId(model.id),
            lot_id=LotId(model.lot_id),
            user_id=UserId(model.user_id),
            amount=model.amount,
            created_at=model.created_at,
        )