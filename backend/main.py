import socketio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
combined_app = socketio.ASGIApp(sio, other_asgi_app=app)

# Store State (Soldier Positions)
game_state = {}


@sio.event
async def connect(sid, environ):
    print(f"Client Connected: {sid}")
    await sio.emit("update_state", game_state, to=sid)


@sio.event
async def telemetry_update(sid, data):
    print(f"Received Telemetry: {data}")
    soldier_id = data.get("id")
    game_state[soldier_id] = data
    await sio.emit("update_state", game_state)


@sio.event
async def disconnect(sid):
    print(f"Client Disconnected: {sid}")


if __name__ == "__main__":
    # IMPORTANT: We run 'combined_app', not 'app'
    uvicorn.run(combined_app, host="0.0.0.0", port=8000)
