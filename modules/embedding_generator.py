
from sentence_transformers import SentenceTransformer
import json
import numpy as np
import os

print("Loading Sentence Transformer model...")

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(video_folder):

    events_path = os.path.join(video_folder, "events.json")

    with open(events_path, "r") as file:
        events = json.load(file)

    texts = []

    for event in events:

        text = (
            f"At {event['timestamp']} seconds, "
            f"{event['description']}. "
            f"Detected objects: {event['objects']}"
        )

        texts.append(text)

    print("\nGenerating embeddings...")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    np.save(
        os.path.join(video_folder, "event_embeddings.npy"),
        embeddings
    )

    metadata = [
        {"timestamp": event["timestamp"], "text": text}
        for event, text in zip(events, texts)
    ]

    with open(
        os.path.join(video_folder, "event_metadata.json"),
        "w"
    ) as file:

        json.dump(metadata, file, indent=4)

    print("\nEmbedding generation completed!")
    print("Total embeddings:", len(embeddings))
    print("Vector dimensions:", embeddings.shape[1])
    print("Saved embeddings successfully!")


if __name__ == "__main__":

    generate_embeddings("outputs/test_video_3ceacd")
