import math
import time
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
STALE_LIMIT = 10  # Seconds before a soldier is marked "stale" (yellow/grey icon)
OFFLINE_LIMIT = 20  # Seconds before deleting the soldier completely
PROTOTYPE_SCALING_FACTOR = 1.5

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
combined_app = socketio.ASGIApp(sio, other_asgi_app=app)

# Store State (Soldier Positions)
game_state = {}
simulator = Simulator()


async def run_threat_sim():
    while True:
        if random.random() > 0.7:
            new_threat = simulator.next_threat()
            await sio.emit("new_threat", new_threat)
            print(f"Sent Threat: {new_threat['id']}")
        await asyncio.sleep(2.5)


async def run_message_sim():
    while True:
        if random.random() > 0.5:
            new_msg = simulator.next_message()
            await sio.emit("new_message", new_msg)
            print(f"Sent Message: {new_msg['id']}")
        await asyncio.sleep(2.5)


async def run_heart_sim():
    while True:
        new_heart = simulator.next_heart_data()
        await sio.emit("new_heart_data", new_heart)
        print(f"Sent Message: {new_heart['id']}")
        await asyncio.sleep(0.2)


async def monitor_stale_data():
    while True:
        current_time = time.time()
        state_changed = False

        for soldier_id in list(game_state.keys()):
            soldier_info = game_state[soldier_id]
            time_since_last_packet = current_time - soldier_info["last_seen"]

            # Condition 1: Soldier has been missing for over 20 seconds (Completely Offline)
            if time_since_last_packet > OFFLINE_LIMIT:
                del game_state[soldier_id]
                state_changed = True

            # Condition 2: Soldier missed their 5-second update window (Stale)
            elif (
                time_since_last_packet > STALE_LIMIT
                and soldier_info["status"] == "active"
            ):
                print(f"[{soldier_id}] Signal lost. Marking as stale.")
                soldier_info["status"] = "stale"
                state_changed = True

        # If someone's status changed to stale or got deleted, update the UI
        if state_changed:
            await sio.emit("update_state", game_state)

        # Pause the loop for 1 second before checking again
        await asyncio.sleep(1)


def calculate_threat_pos(soldier_x, soldier_y, soldier_heading, distances):
    """
    Takes the soldier's 2D position (x, y) and calculates the exact Cartesian (x, y)
    coordinates of all spotted enemies based on their distance and the soldier's heading.
    Assumes standard compass heading (0 = North/Up, 90 = East/Right).
    """
    threats = []

    # Convert compass degrees to radians for the math module
    heading_rad = math.radians(soldier_heading)

    for dist in distances:
        if dist <= 0:
            continue

        # The math to project a point in 2D space using a compass heading
        offset_x = dist * math.sin(heading_rad) * PROTOTYPE_SCALING_FACTOR
        offset_y = (
            dist * math.cos(heading_rad)
            + random.randint(3, 5) * PROTOTYPE_SCALING_FACTOR
        )

        threat_x = soldier_x + offset_x
        threat_y = soldier_y + offset_y

        # Rounding to 2 decimal places (e.g., centimeters) is plenty for a 2D grid
        threats.append(
            {"pos_x": round(threat_x, 2), "pos_y": round(threat_y, 2), "distance": dist}
        )

    return threats


@app.on_event("startup")
async def startup_event():
    sio.start_background_task(run_message_sim)
    sio.start_background_task(run_threat_sim)
    sio.start_background_task(run_heart_sim)
    sio.start_background_task(monitor_stale_data)


@sio.event
async def connect(sid, environ):
    print(f"Client Connected: {sid}")
    await sio.emit("update_state", game_state, to=sid)


@sio.event
async def telemetry_update(sid, data):
    soldier_id = data.get("id")
    if soldier_id is None:
        return

    print(f"[{soldier_id}] Telemetry Received.")

    pos_x, pos_y = data.get("pos", (0, 0))
    heading = data.get("heading", 0)
    raw_distances = data.get("dist", [])

    calculated_threats = calculate_threat_pos(pos_x, pos_y, heading, raw_distances)

    data["calculated_threats"] = calculated_threats

    game_state[soldier_id] = {
        "data": data,
        "last_seen": time.time(),
        "status": "active",
    }

    # Immediately push the fresh data to the frontend
    await sio.emit("update_state", game_state)


@sio.event
async def disconnect(sid):
    print(f"Client Disconnected: {sid}")


if __name__ == "__main__":
    uvicorn.run(combined_app, host="0.0.0.0", port=8000)
