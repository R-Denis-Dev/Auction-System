from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class PlaceBidRequest(BaseModel):
    amount: float = Field(gt=0)


class BidResponse(BaseModel):
    id: int
    lot_id: int
    user_id: int
    amount: float
    created_at: datetime