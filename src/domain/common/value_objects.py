from __future__ import annotations

from dataclasses import dataclass



@dataclass(slots=True, frozen=True)
class Email:
    value:str

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise ValueError("email must be a string")
        if not self.email_pattern:
            raise ValueError(f"Invalid email: {self.value!r}")

    def __str__(self):
        return self.value
    


@dataclass(frozen=True, slots=True)
class HashedPassword:
    value:str   

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise ValueError("hashed_password must be a string")
        if not self.value:
            raise ValueError("hashed_password connot empty")
        
    def __str__(self):
        return self.value
    


@dataclass(frozen=True , slots=True)
class UserID:
    value:int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise ValueError("UserId must be a int")
        if self.value <= 0:
            raise ValueError("UserId must be positive")
        
    def __init__(self):
        return self.value
    
    

@dataclass(frozen=True , slots=True)
class LotID:
    value:int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise ValueError("LotID must be a int")
        if self.value <= 0:
            raise ValueError("LotID must be positive")
        
    def __init__(self):
        return self.value
    


@dataclass(frozen=True , slots=True)
class BidID:
    value:int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise ValueError("BidID must be a int")
        if self.value <= 0:
            raise ValueError("BidID must be positive")
        
    def __init__(self):
        return self.value
