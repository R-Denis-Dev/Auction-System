from __future__ import annotations

from abc import ABC, abstractmethod

from domain.users.entities import User


class IAuthService(ABC):
    @abstractmethod
    async def hash_password(self, plain_password:str) -> str: ...
    @abstractmethod
    async def verify_password(self, plain_password:str, hashed_password:str) -> str:...
    @abstractmethod
    async def create_access_token(self, user:User) -> str: ...
    @abstractmethod
    async def create_refresh_token(self, user:User) -> str: ...