import cv2
import numpy as np
import onnxruntime as ort
from picamera2 import Picamera2
import threading
import time

KNOWN_HEIGHT = 1.7
FOCAL_LENGTH = 600
latest_threat_data: str = ""

print("Loading ONNX model...")
session = ort.InferenceSession("yolo26n.onnx", providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name

print("Warming up camera...")
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 640), "format": "RGB888"}
)
picam2.configure(config)
picam2.start()
time.sleep(2)


def cv_process():
    global latest_threat_data
    try:
        while True:
            frame_rgb = picam2.capture_array()
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

            input_img = frame_rgb.transpose((2, 0, 1))
            input_img = np.expand_dims(input_img, 0).astype(np.float32) / 255.0

            outputs = session.run(None, {input_name: input_img})[0]

            # Squeeze the batch dimension.
            # If the shape is (6, 300), we transpose it to (300, 6) so we can loop through rows cleanly.
            outputs = np.squeeze(outputs)
            if outputs.shape == (6, 300):
                outputs = outputs.T

            humans_distances = []

            for row in outputs:
                # The 6 values directly map to: x1, y1, x2, y2, score, class_id
                x1, y1, x2, y2, score, class_id = row

                # Filter by your confidence threshold and ensure it is a Person (Class 0)
                if score > 0.25 and int(class_id) == 0:

                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    pixel_height = y2 - y1

                    # --- DISTANCE ALGORITHM ---
                    if pixel_height > 0:
                        # Formula: D = (KNOWN_HEIGHT * FOCAL_LENGTH) / pixel_height
                        distance_meters = (KNOWN_HEIGHT * FOCAL_LENGTH) / float(
                            pixel_height
                        )
                    else:
                        distance_meters = 0

                    humans_distances.append(round(distance_meters, 2))

                    # --- DRAWING ---
                    color = (0, 0, 255)
                    cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), color, 2)

                    label = f"THREAT: {round(distance_meters,1)}m"
                    cv2.putText(
                        frame_bgr,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2,
                    )

            threat_data = ",".join([str(int(item)) for item in humans_distances])
            latest_threat_data = threat_data
            print(threat_data)
            # time.sleep(5)

    except KeyboardInterrupt:
        print("\nShutting down gracefully...")

    finally:
        picam2.stop()
        print("Camera released and system offline.")


def get_data():
    """Returns the most recent threat string immediately when called."""
    return latest_threat_data


thread = threading.Thread(target=cv_process, daemon=True)
thread.start()
