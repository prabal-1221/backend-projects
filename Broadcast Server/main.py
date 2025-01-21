from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.usernames: dict[WebSocket, str] = {}
    
    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.usernames[websocket] = username
        await self.broadcast_message(f"{username} has joined the chat", "System")
        await self.broadcast_user_list()
    
    async def disconnect(self, websocket: WebSocket, username: str):
        self.active_connections.remove(websocket)
        self.usernames.pop(websocket, None)
        await self.broadcast_message(f"{username} has left the chat", "System")
        await self.broadcast_user_list()
    
    async def broadcast_message(self, message: str, sender: str):
        for connection in self.active_connections:
            await connection.send_text(f"{sender}: {message}")
    
    async def broadcast_user_list(self):
        user_list = list(self.usernames.values())
        for connection in self.active_connections:
            await connection.send_json({"type": "user_list", "users": user_list})

manager = ConnectionManager()

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    username = websocket.query_params.get("username", "Anonymous")

    await manager.connect(websocket, username)

    try:
        while True:
            message = await websocket.receive_text()
            await manager.broadcast_message(message, username)
    
    except WebSocketDisconnect:
        await manager.disconnect(websocket, username)
