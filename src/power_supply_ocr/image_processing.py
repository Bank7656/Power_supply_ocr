
import cv2
import os
import numpy as np

from paddleocr import PaddleOCR

# Constants
EXIT_FAILURE = 1
GREEN = (0, 255, 0)
RED = (0, 0, 255)
DEFAULT_RESOLUTION = (640, 480)

# Text parameters
text = "Object Detected"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.7
font_thickness = 2

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)

def image_detection(frame):
    frame_resized = cv2.resize(frame, DEFAULT_RESOLUTION)
    voltage, voltage_location = predict_single_number(frame_resized, 105, 55, 110, 70, GREEN)
    current, current_location = predict_single_number(frame_resized, 90, 220, 130, 70, RED)
    display_read_value("Voltage", frame_resized, voltage, voltage_location, GREEN)
    display_read_value("Current", frame_resized, current, current_location, RED)
    cv2.imshow("Power Supply Image detection", frame_resized)
    return frame

def predict_single_number(frame, x, y, w, h, color):
    
    temp_file = "temp.jpg"
    crop_image = frame[y: y + h, x:x + w]
    filtered_image = image_filter(crop_image)

    if not (cv2.imwrite(temp_file, filtered_image)):
        print("Temp file can't be create")
        exit(EXIT_FAILURE)

    result = ocr.predict(temp_file)
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    location = find_text_position(frame, x, y, w, h)
    os.unlink(temp_file)    
    return result, location

def image_filter(img):
    # filtered_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    filtered_img = cv2.GaussianBlur(img, (5, 5), 0)
    kernel = np.ones((1, 1), np.uint8)
    filtered_img = cv2.dilate(filtered_img, kernel, iterations=1)
    # filtered_img = cv2.erode(filtered_img, kernel, iterations=1)
    return img
    

def find_text_position(frame, x, y, w, h):
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_x = x
    padding = 5 # Pixels between the text and the top of the box
    text_y = y - padding # This places the BOTTOM of the text `padding` pixels ABOVE `y`
    if text_y < text_height:
        text_y = text_height + 5
    if text_x < 0:
        text_x = 0
    if text_x + text_width > frame.shape[1]:
        text_x = frame.shape[1] - text_width
    return (text_x, text_y)


def display_read_value(parameter_name, frame, result, loc, color):
    for line in result:
        try:
            text = parameter_name + ": " + line['rec_texts'][0] 
        except IndexError:
            text = parameter_name + ": NaN"
        cv2.putText(img=frame, 
                    text=text, 
                    org=loc, 
                    fontFace=font, 
                    fontScale=font_scale, 
                    color=color, 
                    thickness=font_thickness)
    return