import subprocess
import os
from ultralytics import YOLO
import os

model = YOLO("yolov8n.pt")

def track_objects(video_path):

    os.makedirs("outputs", exist_ok=True)

    results = model.track(
        source=video_path,
        tracker="bytetrack.yaml",
        conf=0.35,
        save=True,
        stream=True,
        project="outputs",
        name="tracked_video",
        exist_ok=True,
        verbose=False
    )

    print("Object tracking started!")

    for result in results:

        if result.boxes.id is not None:

            for box, track_id in zip(result.boxes, result.boxes.id):

                class_id = int(box.cls[0])
                object_name = model.names[class_id]

                print(
                    "Object:", object_name,
                    "| Tracking ID:", int(track_id)
                )

    print("Object tracking completed!")

    output_folder = str(model.predictor.save_dir)

    print("Tracked video location:", output_folder)
    print("Opening tracked video folder...")

    os.startfile(output_folder)


if __name__ == "__main__":
    track_objects("uploads/test_video.mp4")
