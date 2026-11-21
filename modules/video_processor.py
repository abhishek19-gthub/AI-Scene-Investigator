
import cv2
import os

def process_video(video_path, output_folder="outputs/frames", interval=2):

    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video")
        return []

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = total_frames / fps if fps > 0 else 0

    print("Video FPS:", fps)
    print("Video Duration:", round(duration, 2), "seconds")

    extracted_frames = []
    frame_number = 0

    while True:
        success, frame = cap.read()

        if not success:
            break

        timestamp = frame_number / fps if fps > 0 else 0

        if frame_number % max(1, int(fps * interval)) == 0:

            filename = f"frame_{frame_number}.jpg"
            filepath = os.path.join(output_folder, filename)

            cv2.imwrite(filepath, frame)

            extracted_frames.append({
                "frame": frame_number,
                "timestamp": round(timestamp, 2),
                "path": filepath
            })

        frame_number += 1

    cap.release()

    print("Total frames extracted:", len(extracted_frames))

    return extracted_frames


# Step 7: Understand what we built
# Code	Purpose
# cv2.VideoCapture()	Opens the video
# cap.read()	Reads one frame
# CAP_PROP_FPS	Gets video frame rate
# CAP_PROP_FRAME_COUNT	Gets total frames
# cv2.imwrite()	Saves extracted frames
# timestamp	Records when a frame occurs
# interval=2	Extracts one frame every 2 seconds