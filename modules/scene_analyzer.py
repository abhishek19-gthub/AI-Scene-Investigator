
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

print("Loading BLIP model...")

model_name = "Salesforce/blip-image-captioning-base"

processor = BlipProcessor.from_pretrained(model_name)
model = BlipForConditionalGeneration.from_pretrained(model_name)

model.eval()

def analyze_scene(image_path):

    image = Image.open(image_path).convert("RGB")

    inputs = processor(image, return_tensors="pt")

    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=50
        )

    description = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return description


if __name__ == "__main__":

    image_path = "outputs/frames/frame_0.jpg"

    description = analyze_scene(image_path)

    print("\nAI Scene Description:")
    print(description)
