from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Хранилище активных WebSocket-соединений
active_connections: list[WebSocket] = []

@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Отправляем сообщение всем подключённым
            for conn in active_connections:
                await conn.send_text(data)
    except Exception:
        # Убираем соединение при отключении
        if websocket in active_connections:
            active_connections.remove(websocket)
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)