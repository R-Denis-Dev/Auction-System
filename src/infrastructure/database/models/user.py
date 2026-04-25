from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.config import Base
from src.domain.users.entities import UserRole


class UserModel(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email:Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password:Mapped[str] = mapped_column(String(255), nullable=False)
    role:Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.USER)
    is_blocked:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(), nullable=False)
    lots: Mapped[list["LotModel"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    bids: Mapped[list["BidModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )