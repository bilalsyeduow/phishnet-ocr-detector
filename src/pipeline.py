"""
Pipeline module that orchestrates OCR, rules analysis, and scoring.
"""

import sys
from pathlib import Path

# Support running as both `python src/pipeline.py` and `python -m src.pipeline`
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image

from src.ocr import extract_text
from src.rules import analyze_text
from src.scoring import score_risk


def analyze_image(image: Image.Image) -> dict:
    """
    Analyze a PIL Image for phishing indicators.
    
    Args:
        image: PIL Image object to analyze.
    
    Returns:
        Dictionary containing:
        - risk_score: int (0-100)
        - label: str ("Phishing", "Suspicious", "Safe", or "Unknown")
        - confidence: str ("High", "Medium", or "Low")
        - reasons: list[str] of human-readable indicators
        - urls: list[str] of URLs found in the image
        - extracted_text: str full OCR text
        - extracted_text_preview: str first 400 characters
    """
    # Step 1: OCR - Extract text from image
    try:
        extracted_text = extract_text(image)
    except Exception as e:
        # Handle corrupt or unprocessable images
        return {
            "risk_score": 0,
            "label": "Unknown",
            "confidence": "Low",
            "reasons": [f"Failed to process image: {str(e)}"],
            "urls": [],
            "extracted_text": "",
            "extracted_text_preview": "",
        }
    
    # Handle empty OCR result
    if not extracted_text.strip():
        return {
            "risk_score": 0,
            "label": "Unknown",
            "confidence": "Low",
            "reasons": ["No text could be extracted from the image (OCR returned empty)"],
            "urls": [],
            "extracted_text": "",
            "extracted_text_preview": "",
        }
    
    # Step 2: Rules - Analyze text for phishing indicators
    features, reasons, urls = analyze_text(extracted_text)
    
    # Step 3: Scoring - Calculate risk score
    risk_score, label, confidence = score_risk(features)
    
    # Build preview (first 400 chars)
    extracted_text_preview = extracted_text[:400]
    
    return {
        "risk_score": risk_score,
        "label": label,
        "confidence": confidence,
        "reasons": reasons,
        "urls": urls,
        "extracted_text": extracted_text,
        "extracted_text_preview": extracted_text_preview,
    }


def analyze_image_path(path: str) -> dict:
    """
    Analyze an image file for phishing indicators.
    
    Args:
        path: Path to the image file.
    
    Returns:
        Dictionary containing analysis results (same as analyze_image).
    
    Raises:
        FileNotFoundError: If the image file does not exist.
        PIL.UnidentifiedImageError: If the file is not a valid image.
    """
    image = Image.open(path)
    return analyze_image(image)


if __name__ == "__main__":
    import json
    
    test_image_path = "test_images/phish_chat.png"
    
    print(f"Analyzing: {test_image_path}")
    print("-" * 60)
    
    try:
        result = analyze_image_path(test_image_path)
        print(json.dumps(result, indent=2))
    except FileNotFoundError:
        print(f"Error: Image file not found: {test_image_path}")
    except Exception as e:
        print(f"Error analyzing image: {e}")
