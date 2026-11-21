
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from openai import OpenAI


base_path = Path(__file__).resolve().parent.parent
load_dotenv(base_path / ".env")


def offline_answer(question, context):

    lines = [
        line.strip()
        for line in context.splitlines()
        if line.strip()
    ]

    if not lines:
        return "Insufficient video evidence to answer this question."

    timestamps = []
    observations = []
    detected_objects = []

    for line in lines:

        if line.startswith("Timestamp:"):
            timestamps.append(line.replace("Timestamp:", "").strip())

        elif line.startswith("Observation:"):
            observations.append(line.replace("Observation:", "").strip())

            if "Detected objects:" in line:
                detected_objects.append(
                    line.split("Detected objects:", 1)[1].strip()
                )

    answer = "## Video Analysis Report\n\n"

    answer += "### Scene Summary\n"
    answer += (
        "The retrieved video observations indicate:\n\n"
    )

    for observation in observations:
        answer += "- " + observation + "\n"

    answer += "\n### Relevant Timestamps\n"

    for timestamp in timestamps:
        answer += "- " + timestamp + "\n"

    answer += "\n### Detected Objects\n"

    if detected_objects:
        for item in detected_objects:
            answer += "- " + item + "\n"
    else:
        answer += "No object details available.\n"

    answer += (
        "\n### Conclusion\n"
        "This report is based only on locally retrieved "
        "video evidence. No cloud AI service was used."
    )

    return answer


def generate_answer(prompt, question, context):

    provider_mode = os.getenv(
        "LLM_PROVIDER", "auto"
    ).lower()

    # Offline mode
    if provider_mode == "offline":
        print("Using local offline fallback...")
        return offline_answer(question, context), "Offline"

    # Try Gemini first
    if provider_mode in ["auto", "gemini"]:

        api_key = os.getenv("GEMINI_API_KEY")

        if api_key:

            try:
                print("Trying Gemini...")

                client = genai.Client(
                    api_key=api_key
                )

                response = client.models.generate_content(
                    model=os.getenv(
                        "GEMINI_MODEL", "gemini-3.8-flash"
                    ),
                    contents=prompt
                )

                if response.text:
                    return response.text, "Gemini"

            except Exception as e:
                print("Gemini failed:", str(e)[:200])

        else:
            print("Gemini API key not found.")

    # Try Grok second
    if provider_mode in ["auto", "grok"]:

        api_key = os.getenv("XAI_API_KEY")

        if api_key:

            try:
                print("Trying Grok...")

                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.x.ai/v1"
                )

                response = client.responses.create(
                    model=os.getenv(
                        "GROK_MODEL", "grok-4.7"
                    ),
                    input=prompt
                )

                if response.output_text:
                    return response.output_text, "Grok"

            except Exception as e:
                print("Grok failed:", str(e)[:200])

        else:
            print("Grok API key not found.")

    # Final fallback
    print("Using local offline fallback...")

    return offline_answer(question, context), "Offline"
