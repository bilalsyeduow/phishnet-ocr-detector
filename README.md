# PhishNet – OCR-Based Image Phishing Detector

**Author:** Sanaullah Bilal Syed (7598063) – Member 3: Image Phishing Detection

## Overview

PhishNet's Image Phishing Detection module identifies phishing attempts embedded in screenshots and images. It uses OCR to extract text, analyzes content for phishing indicators, evaluates URLs, and produces a risk assessment.

## What This Solves

Traditional phishing detection focuses on email and links, but attackers have moved to:

- **Screenshot Sharing** – Phishing via images in WhatsApp, Telegram bypasses text filters
- **Small-Fee Delivery Scams** – "Pay AED 7.50 to reschedule" leads to credential theft
- **Look-Alike URLs** – Domains with `/verify`, `/login` paths mimicking real services
- **Brand Impersonation** – Fake Emirates Post, bank, LinkedIn messages

## Features

**OCR Text Extraction** – Tesseract-based with preprocessing for screenshots

**Pattern Detection:**
- Urgency language ("act now", "expires in 24 hours")
- Credential requests ("confirm your details", "verify password")
- Brand mentions (Emirates Post, banks, Microsoft, etc.)
- Threat/reward language
- Grammar anomalies

**URL Analysis:**
- Suspicious paths (`/verify`, `/login`, `/update`)
- Shortened links (bit.ly, tinyurl, t.co)
- Suspicious TLDs (.xyz, .top, .click)
- Brand impersonation domains

**Fee Detection** – UAE-specific delivery scam patterns (AED, DHS currency)

## Installation

### Prerequisites

1. Python 3.9+
2. Tesseract OCR (install separately)

### Install Tesseract

**Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki, install to `C:\Program Files\Tesseract-OCR\`

**macOS:** `brew install tesseract`

**Linux:** `sudo apt install tesseract-ocr`

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Project Structure

```
phishnet-ocr-detector/
├── src/
│   ├── ocr.py          # OCR extraction
│   ├── rules.py        # Pattern detection
│   ├── scoring.py      # Risk scoring
│   └── pipeline.py     # Main entry point
├── test_images/        # Sample images
├── app.py              # Streamlit web UI
├── requirements.txt
└── README.md
```

## Usage

### Python API

```python
from src.pipeline import analyze_image_path

result = analyze_image_path("test_images/phish_chat.png")

print(f"Risk Score: {result['risk_score']}/100")
print(f"Label: {result['label']}")
print(f"Reasons: {result['reasons']}")
```

### Streamlit Web App

```bash
streamlit run app.py
```

Open http://localhost:8501 to upload and analyze images.

### Command Line

```bash
python -m src.pipeline
```

## Example Output

```json
{
  "risk_score": 100,
  "label": "Phishing",
  "confidence": "High",
  "reasons": [
    "Urgency language: on hold",
    "Credential request: confirm your details",
    "Brand mentioned: emirates post",
    "Threat language: will be cancelled",
    "Contains URL(s): uae-post-track.com/verify",
    "Fee/payment pressure detected (common delivery scam tactic).",
    "Suspicious keyword in path: verify"
  ],
  "urls": ["uae-post-track.com/verify"],
  "extracted_text_preview": "Emirates Post: Your parcel is on hold..."
}
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `risk_score` | int | 0-100 |
| `label` | str | "Safe", "Suspicious", or "Phishing" |
| `confidence` | str | "Low", "Medium", or "High" |
| `reasons` | list | Human-readable risk factors |
| `urls` | list | URLs found in image |
| `extracted_text` | str | Full OCR output |
| `extracted_text_preview` | str | First 400 chars |

## Integration Example

```python
from src.pipeline import analyze_image_path

def check_image_for_phishing(image_path: str) -> dict:
    result = analyze_image_path(image_path)
    return {
        "is_phishing": result["label"] == "Phishing",
        "risk_score": result["risk_score"],
        "reasons": result["reasons"],
    }
```

## Dependencies

| Package | Purpose |
|---------|---------|
| pytesseract | Tesseract OCR wrapper |
| Pillow | Image processing |
| streamlit | Web interface |

## Notes

- Tesseract must be installed separately and in PATH
- For Windows, edit path in `src/ocr.py` if needed
- Use clear, high-resolution screenshots for best results
- Legitimate urgent messages may occasionally flag as suspicious

## Author

**Sanaullah Bilal Syed** (7598063)
Member 3 – Image Phishing Detection
PhishNet Project
```
---