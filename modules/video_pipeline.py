
import os
import json
import uuid

from pathlib import Path

from modules.video_processor import process_video
from modules.object_detector import detect_objects
from modules.scene_analyzer import analyze_scene
from modules.embedding_generator import generate_embeddings
from modules.vector_store import create_vector_store


def process_video_pipeline(video_path):

    video_path = Path(video_path)

    if not video_path.exists():
        print("Video file not found!")
        return None

    # Create a unique folder for this video
    video_id = video_path.stem + "_" + uuid.uuid4().hex[:6]

    output_folder = Path("outputs") / video_id
    frames_folder = output_folder / "frames"

    os.makedirs(frames_folder, exist_ok=True)

    print("\nProcessing video:", video_path.name)
    print("Video ID:", video_id)

    # Extract video frames
    frames = process_video(
        str(video_path),
        output_folder=str(frames_folder)
    )

    events = []

    # Analyze each frame
    for frame in frames:

        print("\nProcessing frame:", frame["frame"])

        detections = detect_objects(frame["path"])

        description = analyze_scene(frame["path"])

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

    # Save events inside this video's folder
    events_path = output_folder / "events.json"

    with open(events_path, "w") as file:
        json.dump(events, file, indent=4)

    print("\nVideo observations saved!")

    # Generate embeddings
    print("\nGenerating embeddings...")

    generate_embeddings(str(output_folder))

    # Create FAISS vector database
    print("\nCreating vector database...")

    create_vector_store(str(output_folder))

    print("\nComplete video processing pipeline finished!")
    print("Total observations:", len(events))
    print("Video folder:", output_folder)

    return video_id


if __name__ == "__main__":

    video_path = input("Enter video path: ")

    process_video_pipeline(video_path)