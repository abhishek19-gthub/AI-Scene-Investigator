
import json
import faiss
import numpy as np

from pathlib import Path
from modules.llm_provider import generate_answer
from sentence_transformers import SentenceTransformer


print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def ask_video(question, video_folder):

    video_folder = Path(video_folder)

    index_path = (
        video_folder / "vector_store" / "events.index"
    )

    metadata_path = (
        video_folder / "event_metadata.json"
    )

    index = faiss.read_index(str(index_path))

    with open(metadata_path, "r") as file:
        metadata = json.load(file)

    query_embedding = embedding_model.encode(
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
        min(3, index.ntotal)
    )

    context = ""

    for idx in indices[0]:

        if idx == -1:
            continue

        event = metadata[idx]

        context += (
            f"Timestamp: {event['timestamp']} seconds\n"
            f"Observation: {event['text']}\n\n"
        )

    prompt = f"""
You are an AI video analysis assistant.

Answer using only the retrieved video observations.

Rules:
1. Do not invent information.
2. Mention timestamps when relevant.
3. If evidence is insufficient, say so clearly.
4. Do not identify real people.

Video observations:
{context}

Question:
{question}
"""

    answer, provider = generate_answer(
        prompt,
        question,
        context
    )

    print("\nAnswer generated using:", provider)

    return answer


if __name__ == "__main__":

    video_folder = input(
        "Enter video folder path: "
    )

    question = input(
        "\nAsk a question about the video: "
    )

    answer = ask_video(
        question,
        video_folder
    )

    print("\nAI Answer:")
    print(answer)
