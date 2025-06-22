import cv2
import os
import sys
import numpy as np
# import easyocr
# import pytesseract

from paddleocr import PaddleOCR


from PIL import Image

# Constants
EXIT_FAILURE = 1
ESCAPE_KEY = chr(27)
DEFAULT_RESOLUTION = (640, 480)
# reader = easyocr.Reader(['en'])
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False)

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
        if cv2.waitKey(0) & 0xFF == ord(ESCAPE_KEY):
            break
    return 

def image_detection(frame):
    # frame_resized = cv2.resize(frame, DEFAULT_RESOLUTION)
    # cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)

    voltage = predict_single_number(frame, 325, 150, 325, 125)
    # number2 = predict_single_number(frame_resized, 145, 60, 35, 65)
    # number3 = predict_single_number(frame_resized, 175, 60, 35, 65)

    # cv2.imshow("Voltage", frame)    
    # print(f'Voltage = {number1}.{number2}{number3}')
    return

def predict_single_number(frame, x, y, w, h):
    crop_image = frame[y: y + h, x:x + w]
    # img = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
    # kernel = np.ones((1, 1), np.uint8)
    # img = cv2.dilate(img, kernel, iterations=1)
    # img = cv2.erode(img, kernel, iterations=1)
    # img = cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


    temp_file = "temp.jpg"
    cv2.imwrite(temp_file, crop_image)
    result = ocr.predict(temp_file)
    for line in result:
        print(line['rec_texts'])
    os.unlink(temp_file)


    # Process the frame with EasyOCR
    # result = reader.readtext(img, allowlist ='0123456789', detail=0)
    # for (bbox, text, prob) in result:
    #     print(f'Text: {text}, Probability: {prob}')
    # img_new = Image.fromarray(edges)
    # text = pytesseract.image_to_string(img_new, lang='letsgodigital',config='--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789' )
    # try:
    #     print(text[0])
    # except IndexError as e:
    #     print("None")
    # cv2.imshow("Voltage", crop_image)    
    
    cv2.imshow("Voltage", crop_image)
    return None
    


def clear_video(cap):
    cap.release()
    cv2.destroyAllWindows()
    return 