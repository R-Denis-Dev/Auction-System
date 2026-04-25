from __future__ import annotations

from dataclasses import dataclass

from src.application.interfaces.unit_of_work import IUnitOFWork
from src.domain.common.value_objects import LotId


@dataclass
class CancelLotInput:
    lot_id: int
    requester_id: int
    is_admin: bool


class CancelLotUseCase:
    def __init__(self, uow: IUnitOFWork) -> None:
        self._uow = uow

    async def execute(self, data: CancelLotInput) -> None:
        async with self._uow:
            lot = await self._uow.lots.get_by_id(LotId(data.lot_id))
            if lot is None:
                raise ValueError("Lot not found")

            if not data.is_admin and int(lot.owner_id.value) != data.requester_id:
                raise PermissionError("Not allowed to cancel this lot")

            lot.cancel()
            await self._uow.lots.update(lot)