
from modules.object_detector import detect_objects

image_path = "outputs/frames/frame_0.jpg"

detections = detect_objects(image_path)

print("\nDetected Objects:")

for item in detections:
    print(item)
