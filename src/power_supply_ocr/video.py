import cv2
import sys
# import easyocr
# import pytesseract

from power_supply_ocr.image_processing import image_detection
from PIL import Image

# Constants
EXIT_FAILURE = 1
ESCAPE_KEY = chr(27)
DEFAULT_RESOLUTION = (640, 480)


# reader = easyocr.Reader(['en'])


def open_video():
    # Need to fix this for adding many videos
    cap = cv2.VideoCapture("./videos/18_JUN_RUN_4.mp4")
    if not cap.isOpened():
        print("[Exiting Program]")
        sys.exit(EXIT_FAILURE)
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
    # pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
    
    while True:
        success, frame = cap.read()
        if not success:
            print("End of the video or Error reading frame")
            return
        image_detection(frame)
        if cv2.waitKey(1) & 0xFF == ord(ESCAPE_KEY):
            break
    return 

def clear_video(cap):
    cap.release()
    cv2.destroyAllWindows()
    return 