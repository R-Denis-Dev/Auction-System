from __future__ import annotations

from fastapi import FastAPI

from src.presentation.api.routers.auth import router as auth_router
from src.presentation.api.routers.lots import router as lots_router
from src.presentation.api.websockets.lots import router as lots_ws_router



def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(lots_router)
    app.include_router(lots_ws_router)
