from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, Enum, Float, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.config import Base
from src.infrastructure.database.models.user import UserModel
from src.domain.auctions.entities import AuctionStatus


class LotModel(Base):
    __tablename__ = "lots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    start_price: Mapped[float] = mapped_column(Float, nullable=False)
    current_price: Mapped[float] = mapped_column(Float, nullable=False)
    bid_step: Mapped[float] = mapped_column(Float, nullable=False)

    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    status: Mapped[AuctionStatus] = mapped_column(
        Enum(AuctionStatus, name="auction_status"),
        nullable=False,
    )

    is_blocked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    owner: Mapped["UserModel"] = relationship(back_populates="lots")
    bids: Mapped[list["BidModel"]] = relationship(
        back_populates="lot",
        cascade="all, delete-orphan",
    )