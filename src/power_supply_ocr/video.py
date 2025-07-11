import cv2
import sys

from tqdm import tqdm
from power_supply_ocr.data import update_excel
from power_supply_ocr.image_processing import image_detection
from PIL import Image
from tkinter.filedialog import askopenfilename

# Constants
VIDEO_TYPE = ["mov", "mp4"]
EXIT_FAILURE = 1
ESCAPE_KEY = chr(27)
DEFAULT_RESOLUTION = (640, 480)
EMPTY_ROI = (0, 0, 0, 0)
VOLTAGE_SELECTION_PROMPT = "select the area to measure voltage"
CURRENT_SELECTION_PROMPT = "select the area to measure current"

def get_video():
    filepath = askopenfilename()
    if not filepath:
        print("File does not provided!")
        print("[Exiting program]")
        exit(EXIT_FAILURE)
    filename, filetype = filepath.split("/")[-1].split(".")
    print(filepath)
    if filetype not in VIDEO_TYPE:
        print("File type does not support!")
        print("[Exiting program]")
        exit(EXIT_FAILURE)
    return filename, filepath


def open_video(filepath):
    video = cv2.VideoCapture(filepath)
    if not video.isOpened():
        print("Video can't be opened")
        print("[Exiting Program]")
        exit(EXIT_FAILURE)
    fps, total_frames = get_video_detail(video)
    return video, fps, total_frames 
    
def get_video_detail(cap):
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"[Fps: {fps}]")
    print(f"[Resolution: {frame_width} x {frame_height} Total: {total_frames} frames]")
    return fps, total_frames

    
def loop_video(cap, fps, total_frames, sheet) -> None:
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
                roi_voltage, roi_current, status = get_roi(frame_resized)
                if (status):
                    print("Roi were not been chose properly!!!")
                    print("[Exiting program]")
                    clear_video(cap)
                    exit(EXIT_FAILURE)
                    break
                progress_bar = tqdm("Times in video", total=round(total_frames / fps))
            frame, value = image_detection(frame_resized, roi_voltage, roi_current)
            update_excel(sheet, value)
            progress_bar.update(1)
            cv2.imshow("Power Supply Image detection", frame)
        frame_count += 1
    progress_bar.close()
    return 

def get_roi(frame):
    status = 0    
    roi_voltage = cv2.selectROI(VOLTAGE_SELECTION_PROMPT, frame)
    cv2.destroyWindow(VOLTAGE_SELECTION_PROMPT)
    roi_current = cv2.selectROI(CURRENT_SELECTION_PROMPT, frame)
    cv2.destroyWindow(CURRENT_SELECTION_PROMPT)
    if roi_voltage == EMPTY_ROI or roi_current == EMPTY_ROI:
        status = 1
    return roi_voltage, roi_current, status

def clear_video(cap) -> None:
    cap.release()
    cv2.destroyAllWindows()
    return 