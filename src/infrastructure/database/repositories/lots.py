from __future__ import annotations

from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories.lots import ILotRepository
from src.domain.auctions.entities import Lot, AuctionStatus
from src.domain.common.value_objects import LotId, UserId
from src.infrastructure.database.models.lot import LotModel


class LotRepository(ILotRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, lot_id: LotId) -> Lot | None:
        stmt = select(LotModel).where(LotModel.id == int(lot_id.value))
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def list_active(self, now: datetime) -> Sequence[Lot]:
        stmt = (
            select(LotModel)
            .where(LotModel.status == AuctionStatus.ACTIVE)
            .where(LotModel.starts_at <= now)
            .where(LotModel.ends_at > now)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    async def list_by_owner(self, owner_id: UserId) -> Sequence[Lot]:
        stmt = select(LotModel).where(LotModel.owner_id == int(owner_id.value))
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    async def add(self, lot: Lot) -> Lot:
        model = LotModel(
            owner_id=int(lot.owner_id.value),
            title=lot.title,
            description=lot.description,
            start_price=lot.start_price,
            current_price=lot.current_price,
            bid_step=lot.bid_step,
            starts_at=lot.starts_at,
            ends_at=lot.ends_at,
            status=lot.status,
            is_blocked=False,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def update(self, lot: Lot) -> Lot:
        stmt = select(LotModel).where(LotModel.id == int(lot.id.value))
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            raise ValueError("Lot not found")

        model.title = lot.title
        model.description = lot.description
        model.start_price = lot.start_price
        model.current_price = lot.current_price
        model.bid_step = lot.bid_step
        model.starts_at = lot.starts_at
        model.ends_at = lot.ends_at
        model.status = lot.status

        await self._session.flush()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def list_for_ending(self, now: datetime) -> Sequence[Lot]:
        stmt = (
            select(LotModel)
            .where(LotModel.status == AuctionStatus.ACTIVE)
            .where(LotModel.ends_at <= now)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    @staticmethod
    def _to_domain(model: LotModel) -> Lot:
        return Lot(
            id=LotId(model.id),
            owner_id=UserId(model.owner_id),
            title=model.title,
            description=model.description,
            start_price=model.start_price,
            current_price=model.current_price,
            bid_step=model.bid_step,
            starts_at=model.starts_at,
            ends_at=model.ends_at,
            status=model.status
            if isinstance(model.status, AuctionStatus)
            else AuctionStatus(model.status),
        )