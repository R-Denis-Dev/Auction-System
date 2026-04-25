from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Sequence

from src.application.interfaces.unit_of_work import IUnitOFWork


@dataclass
class LotSummary:
    id: int
    owner_id: int
    title: str
    current_price: float
    status: str
    ends_at: datetime


class ListActiveLotsUseCase:
    def __init__(self, uow: IUnitOFWork) -> None:
        self._uow = uow

    async def execute(self) -> Sequence[LotSummary]:
        now = datetime.utcnow()
        async with self._uow:
            lots = await self._uow.lots.list_active(now)

        return [
            LotSummary(
                id=int(l.id.value),
                owner_id=int(l.owner_id.value),
                title=l.title,
                current_price=l.current_price,
                status=l.status.value,
                ends_at=l.ends_at,
            )
            for l in lots
        ]