"""
OCR module using Tesseract via pytesseract for text extraction from images.
"""

import platform
import shutil
from PIL import Image

import pytesseract

# ============================================================================
# TESSERACT CONFIGURATION
# ============================================================================
# Windows fallback path (edit if Tesseract is installed elsewhere)
TESSERACT_CMD_WINDOWS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# ============================================================================


def _configure_tesseract() -> None:
    """Configure Tesseract path based on the operating system."""
    # Try to find tesseract in PATH (works on Mac/Linux, may work on Windows)
    tesseract_path = shutil.which("tesseract")
    
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    elif platform.system() == "Windows":
        # Windows fallback to common install location
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD_WINDOWS


_configure_tesseract()


def _preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess PIL image for OCR: convert to grayscale and apply threshold.

    Args:
        image: Input PIL Image.

    Returns:
        Preprocessed PIL Image (binary/thresholded).
    """
    # Convert to grayscale
    grayscale = image.convert("L")

    # Apply binary threshold (pixels > 128 become white, else black)
    threshold = 128
    binary = grayscale.point(lambda p: 255 if p > threshold else 0)

    return binary


def extract_text(image: Image.Image) -> str:
    """
    Extract text from a PIL Image using Tesseract OCR.

    Args:
        image: Input PIL Image.

    Returns:
        Extracted text as a string.
    """
    # Preprocess: grayscale + threshold
    processed = _preprocess_image(image)

    # Run Tesseract OCR
    text = pytesseract.image_to_string(processed)

    return text.strip()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python src/ocr.py <path/to/image>")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)

    text = extract_text(img)
    print(text)
