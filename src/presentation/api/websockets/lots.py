from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.presentation.api.websockets.manager import manager


router = APIRouter()


@router.websocket("/lots/{lot_id}/ws")
async def lot_websocket(websocket: WebSocket, lot_id: int) -> None:
    await manager.connect(lot_id, websocket)

    try:
        await websocket.send_json(
            {
                "event": "connected",
                "lot_id": lot_id,
                "message": "Subscribed to lot updates",
            }
        )

        while True:
            data = await websocket.receive_text()

            await websocket.send_json(
                {
                    "event": "pong",
                    "lot_id": lot_id,
                    "message": data,
                }
            )

    except WebSocketDisconnect:
        manager.disconnect(lot_id, websocket)