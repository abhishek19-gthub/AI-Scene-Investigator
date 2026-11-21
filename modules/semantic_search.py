
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")


def search_events(question, video_folder, top_k=3):

    index_path = os.path.join(
        video_folder,
        "vector_store",
        "events.index"
    )

    metadata_path = os.path.join(
        video_folder,
        "event_metadata.json"
    )

    index = faiss.read_index(index_path)

    with open(metadata_path, "r") as file:
        metadata = json.load(file)

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    scores, indices = index.search(
        query_embedding,
        min(top_k, index.ntotal)
    )

    print("\nRelevant Video Events:")

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        print("\nTimestamp:", metadata[idx]["timestamp"], "seconds")
        print("Description:", metadata[idx]["text"])
        print("Similarity Score:", round(float(score), 3))


if __name__ == "__main__":

    question = input("Ask a question about the video: ")

    search_events(
        question,
        "outputs/test_video_3ceacd"
    )
