import cv2
from ultralytics import YOLO
import socketio
import math

# 1. Configuration
# ----------------
SERVER_URL = "http://localhost:8000"
MY_LAT = 34.0161
MY_LON = 75.3150
KNOWN_HEIGHT = 1.7  # Average human height (meters)
FOCAL_LENGTH = 600  # Calibration factor (Adjust this later)

sio = socketio.Client()
try:
    sio.connect(SERVER_URL)
    print(f"Connected to Command Server at {SERVER_URL}")
except Exception as e:
    print(f"Failed to connect to server: {e}")
    exit()

print("Loading YOLOv8 model...")
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)  # 0 is usually the default webcam

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Run AI Inference
    results = model(frame, verbose=False)

    enemy_detected = False

    for r in results:
        for box in r.boxes:
            # Class '0' is Person. We assume all people are threats for this demo.
            if int(box.cls[0]) == 0:
                enemy_detected = True

                # Get Bounding Box Dimensions
                x1, y1, x2, y2 = box.xyxy[0]
                pixel_height = y2 - y1

                # --- DISTANCE ALGORITHM ---
                # D = (Real Height * Focal Length) / Image Height
                if pixel_height > 0:
                    distance_meters = (KNOWN_HEIGHT * FOCAL_LENGTH) / float(
                        pixel_height
                    )
                else:
                    distance_meters = 0

                # --- MAPPING ALGORITHM ---
                # We offset the enemy's position slightly North of us based on distance
                # (1 degree lat ~= 111,000 meters)
                offset_lat = distance_meters / 111000.0
                enemy_lat = MY_LAT + offset_lat
                enemy_lon = MY_LON

                # Prepare Data Packet
                threat_data = {
                    "id": "DETECTED-THREAT",
                    "type": "enemy",
                    "lat": enemy_lat,
                    "lon": enemy_lon,
                    "distance": round(distance_meters, 2),
                    "status": "ENGAGING",
                }

                # Send to Dashboard
                sio.emit("telemetry_update", threat_data)

                # Draw on Camera Feed (HUD)
                color = (0, 0, 255)  # Red
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                label = f"THREAT: {round(distance_meters, 1)}m"
                cv2.putText(
                    frame,
                    label,
                    (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2,
                )

    # Show the "Soldier's View"
    cv2.imshow("SENTINEL :: WEAPON SIGHT", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
sio.disconnect()
