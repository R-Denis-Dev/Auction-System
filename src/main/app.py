from __future__ import annotations

from fastapi import FastAPI

from .routers import setup_routers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Auction API",
    )

    setup_routers(app)

    @app.get("/", tags=["test"])
    async def root() -> dict[str, str]:
        return {"message": "Auction API is running"}

    return app


app = create_app()