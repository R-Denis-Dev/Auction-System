from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from src.domain.users.entities import User
from src.domain.common.value_objects import (
    Email, UserId
)

class IUserRepository(Protocol):
    @abstractmethod
    async def get_by_id(self, user_id:UserId) -> User | None: ...
    @abstractmethod
    async def get_by_email(self, email:Email) -> User | None: ...
    @abstractmethod
    async def add(self, user:User) -> User: ...