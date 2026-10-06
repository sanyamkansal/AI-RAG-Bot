import cv2
import pytesseract
import pymupdf
import numpy as np
import os

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def ocr_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray,config="--psm 6")

def ocr_pdf(file_path):
    doc = pymupdf.open(file_path)
    output = ""

    for page in doc:
        pix = page.get_pixmap(dpi=300)
        image = cv2.imdecode(
            np.frombuffer(pix.tobytes("png"), np.uint8),
            cv2.IMREAD_COLOR
        )
        output += ocr_image(image) + "\n"
    doc.close()
    return output

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return ocr_pdf(file_path)

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    if ext in [".png", ".jpg", ".jpeg"]:
        image = cv2.imread(file_path)

        if image is None:
            raise ValueError(f"Could not read file: {file_path}")
        
        return ocr_image(image)

    raise ValueError(f"Unsupported file type: {ext}")