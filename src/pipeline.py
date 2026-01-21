"""Pipeline module that orchestrates OCR, rules analysis, and scoring."""

import sys
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image

from src.ocr import extract_text
from src.rules import analyze_text
from src.scoring import score_risk


def analyze_image(image: Image.Image) -> dict:
    """Analyze a PIL Image for phishing indicators."""
    try:
        extracted_text = extract_text(image)
    except Exception as e:
        return {
            "risk_score": 0,
            "label": "Unknown",
            "confidence": "Low",
            "reasons": [f"Failed to process image: {str(e)}"],
            "urls": [],
            "extracted_text": "",
            "extracted_text_preview": "",
        }
    
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
    
    features, reasons, urls = analyze_text(extracted_text)
    risk_score, label, confidence = score_risk(features)
    
    # 400 chars is usually enough for a preview
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
    """Analyze an image file for phishing indicators."""
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
