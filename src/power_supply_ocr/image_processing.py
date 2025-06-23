
import cv2
import os
import numpy as np

from paddleocr import PaddleOCR


# Text parameters
text = "Object Detected"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.7
font_thickness = 2
GREEN = (0, 255, 0)
RED = (0, 0, 255)

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False)

def image_detection(frame):
    # frame_resized = cv2.resize(frame, DEFAULT_RESOLUTION)

    voltage, voltage_location = predict_single_number(frame, 325, 150, 325, 125, GREEN)
    current, current_location = predict_single_number(frame, 260, 500, 400, 150, RED)

    
    display_read_value("Voltage", frame, voltage, voltage_location, GREEN)
    display_read_value("Current", frame, current, current_location, RED)
    cv2.imshow("Power Supply Image detection", frame)
    return frame

def predict_single_number(frame, x, y, w, h, color):
    crop_image = frame[y: y + h, x:x + w]
    crop_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
    # kernel = np.ones((1, 1), np.uint8)
    # img = cv2.dilate(img, kernel, iterations=1)
    # img = cv2.erode(img, kernel, iterations=1)
    # img = cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    temp_file = "temp.jpg"
    cv2.imwrite(temp_file, crop_image)
    result = ocr.predict(temp_file)
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    location = find_text_position(frame, x, y, w, h)
    os.unlink(temp_file)

    # Process the frame with EasyOCR
    # result = reader.readtext(img, allowlist ='0123456789', detail=0)
    # for (bbox, text, prob) in result:
    #     print(f'Text: {text}, Probability: {prob}')
    # img_new = Image.fromarray(edges)
    # text = pytesseract.image_to_string(img_new, lang='letsgodigital',config='--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789' )
    # try:
    #     print(text[0)
    # except IndexError as e:
    #     print("None")
    # cv2.imshow("Voltage", crop_image)
    
    return result, location
    

def find_text_position(frame, x, y, w, h):
    # Calculate text size to get its height, which is crucial for positioning
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)

    # Position for the text:
    # text_x will be the 'x' of the rectangle (left edge)
    text_x = x

    # text_y needs to be calculated to place the text *above* the rectangle.
    # Remember cv2.putText uses the bottom-left corner of the text.
    # So, to place the text 'padding' pixels above the rectangle's top edge (y):
    # text_y = y (top of rectangle) - padding
    # Since y is the bottom of the text, we subtract the text_height to get to its top,
    # and then subtract padding to move it further up.
    padding = 5 # Pixels between the text and the top of the box
    text_y = y - padding # This places the BOTTOM of the text `padding` pixels ABOVE `y`

    # Important: If the text is too large, text_y could become negative, making it go off-screen.
    # You might want to add a check for this:
    if text_y < text_height: # If the top of the text would be off-screen
        text_y = text_height + 5 # Place it at the very top with a small margin

    # Add a check for horizontal bounds too
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