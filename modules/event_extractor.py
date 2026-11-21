
import json
import os

from modules.video_processor import process_video
from modules.object_detector import detect_objects
from modules.scene_analyzer import analyze_scene


def extract_events(video_path):

    print("Starting event extraction...")

    frames = process_video(video_path)

    events = []

    for frame in frames:

        print("\nProcessing frame:", frame["frame"])

        # Get YOLO detections
        detections = detect_objects(frame["path"])

        # Get BLIP description
        description = analyze_scene(frame["path"])

        # Count detected objects
        object_counts = {}

        for item in detections:

            name = item["object"]

            object_counts[name] = object_counts.get(name, 0) + 1

        event = {
            "timestamp": frame["timestamp"],
            "description": description,
            "objects": object_counts,
            "detections": detections
        }

        events.append(event)

        print("Description:", description)
        print("Objects:", object_counts)

    # Save events as JSON
    os.makedirs("outputs", exist_ok=True)

    with open("outputs/events.json", "w") as file:
        json.dump(events, file, indent=4)

    print("\nEvent extraction completed!")
    print("Total observations:", len(events))
    print("Saved to outputs/events.json")

    return events


if __name__ == "__main__":

    extract_events("uploads/test_video.mp4")
