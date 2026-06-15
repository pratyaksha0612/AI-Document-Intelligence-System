import cv2
from modules.image_processor import preprocess_image
from modules.ocr_engine import extract_text, get_text_data
from modules.confidence_analyzer import calculate_average_confidence
from modules.information_extractor import extract_information
from modules.text_cleaner import clean_ocr_text

# Load image
image = cv2.imread("assets/sample_invoice.png")

# Preprocess image
gray, blurred, threshold = preprocess_image(image)

cv2.imwrite(
    "outputs/processed_image.jpg",
    threshold
)

# OCR
text = extract_text(threshold)
text = clean_ocr_text(text)

# Confidence
data = get_text_data(threshold)
confidence = calculate_average_confidence(data)

# Information Extraction
info = extract_information(text)

print("\n===== EXTRACTED TEXT =====\n")
print(text)

print("\n===== OCR CONFIDENCE =====\n")
print(f"{confidence}%")

print("\n===== EXTRACTED INFORMATION =====\n")

for key, value in info.items():
    print(f"{key}: {value}")