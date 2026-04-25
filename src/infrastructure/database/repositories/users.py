from __future__ import annotations

from typing import Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories.users import IUserRepository
from src.domain.common.value_objects import (
    Email,
    HashedPassword,
    UserId
)
from src.domain.users.entities import User, UserRole
from src.infrastructure.database.models.user import UserModel


class UserRepository(IUserRepository):
    def __init__(self, session:AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id:UserId) -> User | None:
        res = select(UserModel).where(UserModel.id == int(user_id))
        result = await self._session.execute(res)
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return self._to_domain(row)
        
    async def get_by_email(self, email:Email) -> User | None:
        res = select(UserModel).where(UserModel.email == str(email))
        result = await self._session.execute(res)
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return self._to_domain(row)
    
    async def add(self, user:User) -> User:
        model = UserModel(
            email=str(user.email),
            hashed_password=user.password.value,
            role=user.role,
            is_blocked=user.is_blocked,
            created_at=user.created_at
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_domain(model)
    
    @staticmethod
    def _to_domain(model:UserModel):
        return User(
            id=UserId(model.id),
            email=Email(model.email),
            password=HashedPassword(model.hashed_password),
            role=model.role if isinstance(model.role, UserRole) else UserRole(model.role),
            is_blocked=model.is_blocked,
            created_at=model.created_at
        )
    