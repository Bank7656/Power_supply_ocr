import cv2
import sys

ESCAPE_KEY = chr(27)

def open_video():
    # Need to fix this for adding many videos
    cap = cv2.VideoCapture("./videos/18_JUN_RUN_4.mp4")
    if not cap.isOpened():
        print("[Exiting Program]")
        sys.exit(1)
    
    get_video_detail(cap)
    return cap
    
def get_video_detail(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Fps: {fps}")
    print(f"Resolution: {frame_width} x {frame_height} Total: {total_frames} frames")

    
def loop_video(cap):
    while True:
        # Read a frame from a video
        success, frame = cap.read()
        if not success:
            print("End of the video or Error reading frame")
            return
        cv2.imshow('Power_supply_ocr', frame)

        if cv2.waitKey(1) & 0xFF == ord(ESCAPE_KEY):
            break
    return 

def clear_video(cap):
    cap.release()
    cv2.destroyAllWindows()
    return 