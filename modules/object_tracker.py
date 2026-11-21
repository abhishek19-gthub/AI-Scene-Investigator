
import os
import cv2
from ultralytics import YOLO


def create_annotated_video(video_path, output_path, confidence=0.35):

    video_path = str(video_path)
    output_path = str(output_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Unable to open input video.")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 25

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Ensure dimensions are even for video encoding
    width = width - (width % 2)
    height = height - (height % 2)

    fourcc = cv2.VideoWriter_fourcc(*"avc1")

    writer = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    if not writer.isOpened():
        cap.release()
        raise RuntimeError(
            "H.264 video encoder is unavailable. "
            "Please install an FFmpeg-enabled OpenCV build."
        )

    model = YOLO("yolov8n.pt")

    frame_count = 0

    try:

        while True:

            success, frame = cap.read()

            if not success:
                break

            frame = cv2.resize(frame, (width, height))

            results = model.track(
                source=frame,
                persist=True,
                tracker="bytetrack.yaml",
                conf=confidence,
                verbose=False
            )

            annotated_frame = results[0].plot()

            writer.write(annotated_frame)

            frame_count += 1

            if frame_count % 100 == 0:
                print("Annotated frames:", frame_count)

    finally:

        cap.release()
        writer.release()

    if frame_count == 0:
        raise RuntimeError("No frames were processed.")

    print("Annotated video created:", output_path)
    print("Total annotated frames:", frame_count)

    return output_path


# Original tracking function retained for standalone testing
def track_objects(video_path):

    os.makedirs("outputs", exist_ok=True)

    output_path = os.path.join(
        "outputs",
        "tracked_video.mp4"
    )

    create_annotated_video(video_path, output_path)

    if os.name == "nt":
        os.startfile(os.path.dirname(output_path))


if __name__ == "__main__":

    track_objects("uploads/test_video.mp4")
