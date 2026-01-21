"""OCR module using Tesseract via pytesseract for text extraction from images."""

import platform
import shutil
from PIL import Image

import pytesseract

TESSERACT_CMD_WINDOWS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def _configure_tesseract():
    """Configure Tesseract path based on the operating system."""
    tesseract_path = shutil.which("tesseract")
    
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    elif platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD_WINDOWS


_configure_tesseract()


def _preprocess_image(image):
    """Preprocess PIL image for OCR: grayscale + threshold."""
    grayscale = image.convert("L")

    threshold = 128  # seems to work well for most screenshots
    binary = grayscale.point(lambda p: 255 if p > threshold else 0)

    return binary


def extract_text(image: Image.Image) -> str:
    """Extract text from a PIL Image using Tesseract OCR."""
    processed = _preprocess_image(image)
    text = pytesseract.image_to_string(processed)

    return text.strip()
