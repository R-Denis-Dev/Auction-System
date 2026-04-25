from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.application.interfaces.unit_of_work import IUnitOFWork
from src.domain.common.value_objects import LotId


@dataclass
class GetLotInput:
    lot_id: int


@dataclass
class GetLotOutput:
    id: int
    owner_id: int
    title: str
    description: str
    current_price: float
    start_price: float
    bid_step: float
    status: str
    starts_at: datetime
    ends_at: datetime


class GetLotUseCase:
    def __init__(self, uow: IUnitOFWork) -> None:
        self._uow = uow

    async def execute(self, data: GetLotInput) -> GetLotOutput:
        async with self._uow:
            lot = await self._uow.lots.get_by_id(LotId(data.lot_id))

        if lot is None:
            raise ValueError("Lot not found")

        return GetLotOutput(
            id=int(lot.id.value),
            owner_id=int(lot.owner_id.value),
            title=lot.title,
            description=lot.description,
            current_price=lot.current_price,
            start_price=lot.start_price,
            bid_step=lot.bid_step,
            status=lot.status.value,
            starts_at=lot.starts_at,
            ends_at=lot.ends_at,
        )