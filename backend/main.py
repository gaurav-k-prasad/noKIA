import socketio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from simulator import Simulator
import asyncio
import random

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
simulator = Simulator()


async def run_simulation():
    print("Simulation started!")  # Added to confirm it's running
    while True:
        if random.random() > 0.7:
            new_threat = simulator.next_threat()
            await sio.emit("new_threat", new_threat)
            print(f"Sent Threat: {new_threat['id']}")

        if random.random() > 0.5:
            new_msg = simulator.next_message()
            await sio.emit("new_message", new_msg)
            print(f"Sent Message: {new_msg['id']}")

        await asyncio.sleep(0.2)


@app.on_event("startup")
async def startup_event():
    sio.start_background_task(run_simulation)


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
    uvicorn.run(combined_app, host="0.0.0.0", port=8000)
