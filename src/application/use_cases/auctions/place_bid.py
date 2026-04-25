from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from src.application.interfaces.unit_of_work import IUnitOFWork
from src.domain.auctions.entities import Bid
from src.domain.common.value_objects import LotId, UserId, BidId


@dataclass
class PlaceBidInput:
    lot_id: int
    user_id: int
    amount: float


@dataclass
class PlaceBidOutput:
    lot_id: int
    current_price: float
    status: str


class PlaceBidUseCase:
    def __init__(self, uow: IUnitOFWork) -> None:
        self._uow = uow

    async def execute(self, data: PlaceBidInput) -> PlaceBidOutput:
        now = datetime.utcnow()

        async with self._uow:
            lot = await self._uow.lots.get_by_id(LotId(data.lot_id))
            if lot is None:
                raise ValueError("Lot not found")

            lot.apply_bid(
                amount=data.amount,
                bidder_id=UserId(data.user_id),
                now=now,
            )

            bid = Bid(
                id=BidId,
                lot_id=lot.id,
                user_id=UserId(data.user_id),
                amount=data.amount,
                created_at=now,
            )

            await self._uow.bids.add(bid)
            await self._uow.lots.update(lot)

        return PlaceBidOutput(
            lot_id=data.lot_id,
            current_price=lot.current_price,
            status=lot.status.value,
        )