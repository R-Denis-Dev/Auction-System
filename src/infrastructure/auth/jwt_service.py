from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any, Dict

import jwt

from application.interfaces.auth import IAuthService
from domain.users.entities import User


class JwtAuthService(IAuthService):
    def __init__(
            self,
            secret_key:str,
            algorithm:str = "HS256",
            access_token_expires_minutes: int = 30,
            refresh_token_expires_days: int = 7
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm        
        self._access_token_expires_minutes = access_token_expires_minutes
        self._refresh_token_expires_days = refresh_token_expires_days

    def _create_token(self, user:User, expires_delta:timedelta) -> str:
        now = datetime.now(timezone.utc)
        payload:Dict[str, Any] = { 
            "sub":str(user.id.value),
            "role":user.role.value,
            "iat":now,
            "exp": now + expires_delta
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
    
    def hash_password(self, plain_password: str) -> str:
        raise NotImplementedError("Use PasswordHasher directly for hashing")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError("Use PasswordHasher directly for verifying")

    def create_access_token(self, user: User) -> str:
        return self._create_token(user, timedelta(minutes=self._access_exp))

    def create_refresh_token(self, user: User) -> str:
        return self._create_token(user, timedelta(days=self._refresh_exp))
    