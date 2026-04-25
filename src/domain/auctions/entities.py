from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from src.domain.common.value_objects import UserId, LotId, BidId


class AuctionStatus(str, Enum):
    ACTIVE = "active"
    ENDED = "ended"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class Lot:
    id: LotId
    owner_id: UserId
    title: str
    description: str
    start_price: float
    current_price: float
    bid_step: float
    starts_at: datetime
    ends_at: datetime
    status: AuctionStatus

    def can_place_bid(self, now: datetime) -> bool:
        if self.status != AuctionStatus.ACTIVE:
            return False
        if now < self.starts_at:
            return False
        if now >= self.ends_at:
            return False
        return True

    def min_allowed_bid(self) -> float:
        if self.current_price <= 0:
            return self.start_price
        return self.current_price + self.bid_step

    def apply_bid(
        self,
        amount: float,
        bidder_id: UserId,
        now: datetime,
        anti_sniping_last_seconds: int | None = None,
        anti_sniping_extend_seconds: int | None = None,
    ) -> None:
        if not self.can_place_bid(now):
            raise ValueError("Cannot place bid on this lot now")

        min_amount = self.min_allowed_bid()
        if amount < min_amount:
            raise ValueError(f"Bid is too low, min allowed is {min_amount}")

        self.current_price = amount

        if (
            anti_sniping_last_seconds is not None
            and anti_sniping_extend_seconds is not None
        ):
            remaining = (self.ends_at - now).total_seconds()
            if 0 <= remaining <= anti_sniping_last_seconds:
                self.ends_at = self.ends_at.replace() + timedelta(
                    seconds=anti_sniping_extend_seconds
                )

    def cancel(self) -> None:
        if self.status == AuctionStatus.ENDED:
            raise ValueError("Cannot cancel an ended auction")
        self.status = AuctionStatus.CANCELLED

    def end(self) -> None:
        self.status = AuctionStatus.ENDED


@dataclass(slots=True)
class Bid:
    id: BidId | None
    lot_id: LotId
    user_id: UserId
    amount: float
    created_at: datetime