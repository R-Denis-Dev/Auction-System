from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from src.application.interfaces.unit_of_work import IUnitOFWork
from src.domain.auctions.entities import Lot, AuctionStatus
from src.domain.common.value_objects import LotId, UserId


@dataclass
class CreateLotInput:
    owner_id: int
    title: str
    description: str
    start_price: float
    bid_step: float
    starts_at: datetime
    ends_at: datetime


@dataclass
class CreateLotOutput:
    id: int
    owner_id: int
    title: str
    description: str
    current_price: float
    status: str
    starts_at: datetime
    ends_at: datetime


class CreateLotUseCase:
    def __init__(self, uow: IUnitOFWork) -> None:
        self._uow = uow

    async def execute(self, data: CreateLotInput) -> CreateLotOutput:
        now = datetime.utcnow()
        lot = Lot(
            id=LotId, 
            owner_id=UserId(data.owner_id),
            title=data.title,
            description=data.description,
            start_price=data.start_price,
            current_price=data.start_price,
            bid_step=data.bid_step,
            starts_at=data.starts_at,
            ends_at=data.ends_at,
            status=AuctionStatus.ACTIVE,
        )

        async with self._uow:
            created = await self._uow.lots.add(lot)

        return CreateLotOutput(
            id=int(created.id.value),
            owner_id=int(created.owner_id.value),
            title=created.title,
            description=created.description,
            current_price=created.current_price,
            status=created.status.value,
            starts_at=created.starts_at,
            ends_at=created.ends_at,
        )