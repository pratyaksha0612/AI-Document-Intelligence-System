import re


def clean_ocr_text(text):

    text = re.sub(r'75,(\d{3})', r'5,\1', text)

    return text