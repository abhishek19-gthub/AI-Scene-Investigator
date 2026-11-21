
from ultralytics import YOLO
import cv2
import os

# Load lightweight YOLO model
model = YOLO("yolov8n.pt")

def detect_objects(image_path):

    results = model(image_path, conf=0.35, verbose=False)

    os.makedirs("outputs/detections", exist_ok=True)

    detections = []

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            object_name = model.names[class_id]
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detections.append({
                "object": object_name,
                "confidence": round(confidence, 2),
                "box": [x1, y1, x2, y2]
            })

        # Save image with bounding boxes
        annotated_image = result.plot()

        output_path = "outputs/detections/detected_frame.jpg"

        cv2.imwrite(output_path, annotated_image)

    return detections
