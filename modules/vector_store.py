
import faiss
import numpy as np
import os


def create_vector_store(video_folder):

    print("Loading embeddings...")

    embeddings_path = os.path.join(
        video_folder,
        "event_embeddings.npy"
    )

    embeddings = np.load(embeddings_path)

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    print("Creating FAISS index...")

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    vector_folder = os.path.join(
        video_folder,
        "vector_store"
    )

    os.makedirs(vector_folder, exist_ok=True)

    index_path = os.path.join(
        vector_folder,
        "events.index"
    )

    faiss.write_index(index, index_path)

    print("\nFAISS Vector Database Created!")
    print("Total vectors:", index.ntotal)
    print("Vector dimensions:", dimension)
    print("Saved to:", index_path)


if __name__ == "__main__":

    create_vector_store("outputs/test_video_3ceacd")
