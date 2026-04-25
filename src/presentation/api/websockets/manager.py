from __future__ import annotations

from collections import defaultdict

from fastapi import WebSocket


class LotConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, lot_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[lot_id].append(websocket)

    def disconnect(self, lot_id: int, websocket: WebSocket) -> None:
        if lot_id in self._connections and websocket in self._connections[lot_id]:
            self._connections[lot_id].remove(websocket)

        if lot_id in self._connections and not self._connections[lot_id]:
            del self._connections[lot_id]

    async def broadcast_to_lot(self, lot_id: int, message: dict) -> None:
        dead_connections: list[WebSocket] = []

        for websocket in self._connections.get(lot_id, []):
            try:
                await websocket.send_json(message)
            except Exception:
                dead_connections.append(websocket)

        for websocket in dead_connections:
            self.disconnect(lot_id, websocket)


manager = LotConnectionManager()