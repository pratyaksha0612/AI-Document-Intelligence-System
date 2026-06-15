import cv2


def preprocess_image(image):

    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Upscale image
    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Noise reduction
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Binary threshold + invert
    threshold = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]

    return gray, blurred, threshold