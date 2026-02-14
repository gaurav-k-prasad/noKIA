import cv2
import numpy as np
import onnxruntime as ort
import socketio

SERVER_URL = "http://localhost:8000"
KNOWN_HEIGHT = 1.7
FOCAL_LENGTH = 600

sio = socketio.Client()
sio.connect(SERVER_URL)

print("Loading ONNX model...")
session = ort.InferenceSession("yolo26n.onnx", providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name

pos_x = 200
pos_y = 170
heading = 120

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img = cv2.resize(frame, (640, 640))
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)

    outputs = session.run(None, {input_name: img})
    predictions = outputs[0][0]

    humans_distances = []

    for pred in predictions:
        conf = pred[4]
        cls = np.argmax(pred[5:])

        if conf > 0.5 and cls == 0:
            x, y, w, h = pred[0:4]

            pixel_height = h * frame.shape[0] / 640

            if pixel_height > 0:
                distance = (KNOWN_HEIGHT * FOCAL_LENGTH) / pixel_height
            else:
                distance = 0

            humans_distances.append(round(distance, 2))

    threat_data = {
        "id": 0,
        "dist": humans_distances,
        "pos": (pos_x, pos_y),
        "heading": heading,
    }

    sio.emit("telemetry_update", threat_data)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
sio.disconnect()
