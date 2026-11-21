
import json
import os
import re


def clean_text(text):

    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text


def process_events():

    with open("outputs/events.json", "r") as file:
        events = json.load(file)

    processed_events = []

    for event in events:

        timestamp = event["timestamp"]
        description = clean_text(event["description"])

        objects = event["objects"]

        object_text = []

        for name, count in objects.items():

            object_text.append(
                f"{count} {name}(s)"
            )

        object_summary = ", ".join(object_text)

        text = (
            f"At {timestamp} seconds, "
            f"{description}. "
            f"Detected objects include {object_summary}."
        )

        processed_events.append({
            "timestamp": timestamp,
            "text": text
        })

    os.makedirs("outputs", exist_ok=True)

    with open("outputs/processed_events.json", "w") as file:
        json.dump(processed_events, file, indent=4)

    print("NLP processing completed!")
    print("Total processed events:", len(processed_events))
    print("Saved to outputs/processed_events.json")

    return processed_events


if __name__ == "__main__":

    results = process_events()

    for item in results:
        print("\n", item["text"])
