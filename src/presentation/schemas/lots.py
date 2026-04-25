from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class CreateLotRequest(BaseModel):
    title: str = Field(max_length=255)
    description: str
    start_price: float = Field(gt=0)
    bid_step: float = Field(gt=0)
    starts_at: datetime
    ends_at: datetime


class LotResponse(BaseModel):
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


class LotSummaryResponse(BaseModel):
    id: int
    owner_id: int
    title: str
    current_price: float
    status: str
    ends_at: datetime