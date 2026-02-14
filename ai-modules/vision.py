import cv2
from ultralytics import YOLO  # type: ignore
import socketio

# INFO - Change server url in R-Pi
SERVER_URL = "http://localhost:8000"
KNOWN_HEIGHT = 1.7


FOCAL_LENGTH = 600

sio = socketio.Client()
try:
    sio.connect(SERVER_URL)
    print(f"Connected to Command Server at {SERVER_URL}")
except Exception as e:
    print(f"Failed to connect to server: {e}")
    exit()

print("Loading YOLOv8 model...")
model = YOLO("yolo26n.pt")


# ! warning get the values from gps
pos_x = 200
pos_y = 170
heading = 120

# INFO - change for capturing video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    results = model(frame, verbose=False)
    humans_distances = []

    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:  # class 0 is person
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
                humans_distances.append(
                    round(distance_meters, 2),
                )

                color = (0, 0, 255)
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

    threat_data = {
        "id": 0,  # ! WARNING ID IS HARDCODED
        "dist": humans_distances,
        "pos": (pos_x, pos_y),
        "heading": heading,
    }

    # ! WARNING - SLOW DOWN NO NEED TO SEND DATA THAT FAST
    sio.emit("telemetry_update", threat_data)
    # INFO - transmit the data no need to show in raspberry pi
    cv2.imshow("SENTINEL :: WEAPON SIGHT", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
sio.disconnect()
