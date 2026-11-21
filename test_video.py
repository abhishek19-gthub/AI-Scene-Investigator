
from modules.video_processor import process_video

frames = process_video("uploads/test_video.mp4")

for frame in frames:
    print(frame)
