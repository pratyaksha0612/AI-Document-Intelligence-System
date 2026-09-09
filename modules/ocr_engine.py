import cv2
import pytesseract
import os
import platform

# Set Tesseract Path
if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image):

    custom_config = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(
        image,
        lang='eng',
        config=custom_config
    )

    return text


def get_text_data(image):

    data = pytesseract.image_to_data(
        image,
        config='--oem 3 --psm 6',
        output_type=pytesseract.Output.DICT
    )

    return data


def draw_bounding_boxes(image):

    data = get_text_data(image)

    boxed_image = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2BGR)

    n_boxes = len(data["text"])

    for i in range(n_boxes):

        try:
            confidence = float(data["conf"][i])
        except:
            confidence = 0

        if confidence > 40:

            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]

            cv2.rectangle(
                boxed_image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

    return boxed_image