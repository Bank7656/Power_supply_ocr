import cv2
import sys

from power_supply_ocr.image_processing import image_detection
from PIL import Image

# Constants
EXIT_FAILURE = 1
ESCAPE_KEY = chr(27)
DEFAULT_RESOLUTION = (640, 480)
VOLTAGE_SELECTION_PROMPT = "select the area to measure voltage"
CURRENT_SELECTION_PROMPT = "select the area to measure current"

def open_video():
    cap = cv2.VideoCapture("./videos/18_JUN_RUN_4.mp4")
    if not cap.isOpened():
        print("[Exiting Program]")
        sys.exit(EXIT_FAILURE)
    fps = get_video_detail(cap)
    return cap, fps
    
def get_video_detail(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"[Fps: {fps}]")
    print(f"[Resolution: {frame_width} x {frame_height} Total: {total_frames} frames]")
    return fps

    
def loop_video(cap, fps):
    frame_count = 0
    while True:
        success, frame = cap.read()

        if not success:
            print("End of the video or Error reading frame")
            return

        if cv2.waitKey(1) & 0xFF == ord(ESCAPE_KEY):
            break
    
        if frame_count % fps == 0:
            frame_resized = cv2.resize(frame, DEFAULT_RESOLUTION)
            if frame_count == 0:
                roi_voltage = cv2.selectROI(VOLTAGE_SELECTION_PROMPT, frame_resized)
                cv2.destroyWindow(VOLTAGE_SELECTION_PROMPT)
                roi_current = cv2.selectROI(CURRENT_SELECTION_PROMPT, frame_resized)
                cv2.destroyWindow(CURRENT_SELECTION_PROMPT)
                if roi_voltage == (0, 0, 0, 0) or roi_current == (0, 0, 0, 0):
                    print("Both roi were not detected propely!!")
                    print("[Exiting Program]")
                    break
            image_detection(frame_resized, roi_voltage, roi_current)
        frame_count += 1
    return 

def clear_video(cap):
    cap.release()
    cv2.destroyAllWindows()
    return 