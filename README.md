# PhishNet – OCR-Based Image Phishing Detector

**Author:** Sanaullah Bilal Syed (7598063) – Member 3: Image Phishing Detection

---

## Overview

PhishNet's Image Phishing Detection module identifies **phishing attempts embedded in screenshots and images**. Unlike traditional email/URL scanners, this module targets modern attack vectors where phishing content is delivered as images—bypassing conventional text-based filters.

The system extracts text from images using OCR (Optical Character Recognition), analyzes the content for phishing indicators, evaluates URL plausibility, and produces an **explainable risk assessment** with actionable insights.

---

## What This Solves

### The Modern Phishing Landscape

Traditional phishing detection focuses on email headers, link analysis, and text content. However, attackers have evolved:

| Attack Vector | Description |
|---------------|-------------|
| **Screenshot Sharing** | Phishing messages shared as images in WhatsApp, Telegram, and other chat apps completely bypass email and SMS filters |
| **AI-Generated Content** | Realistic, grammatically correct messages with subtle urgency and psychological pressure |
| **Small-Fee Delivery Scams** | "Pay AED 7.50 to reschedule delivery" – low amounts that seem legitimate but lead to credential theft |
| **Look-Alike URLs** | Domains with suspicious paths like `/verify`, `/login`, `/update` that mimic legitimate services |
| **Brand Impersonation** | Fake messages from Emirates Post, banks, LinkedIn, and other trusted entities |

This module specifically targets these modern patterns rather than obvious spam indicators.

---

## Features

### 1. OCR Text Extraction

- **Input:** Screenshot or image file (PNG, JPG, JPEG, BMP, TIFF)
- **Output:** Extracted text with preview
- **Engine:** Tesseract OCR with optimized preprocessing

### 2. Explainable Phishing Analysis

Rule-based detection system that identifies and explains each risk factor:

| Pattern | Examples |
|---------|----------|
| **Urgency Language** | "immediate action required", "expires in 24 hours", "act now" |
| **Credential Requests** | "confirm your details", "verify your password", "update your information" |
| **Brand Impersonation** | Emirates Post, banks, LinkedIn, Microsoft, Apple, PayPal |
| **Threat Language** | "account will be suspended", "will be cancelled", "access restricted" |
| **Reward Bait** | "you won", "congratulations", "claim your prize" |
| **Grammar/Format Anomalies** | Unusual capitalization, suspicious formatting patterns |
| **URL Presence** | Detection and extraction of embedded URLs |

### 3. URL Plausibility Heuristics

Advanced URL analysis for modern phishing indicators:

- **Suspicious Path Keywords:** `/verify`, `/login`, `/update`, `/confirm`, `/secure`
- **Domain Structure:** Multiple hyphens in domain (e.g., `bank-secure-login.com`)
- **Shortened Links:** bit.ly, tinyurl, t.co, goo.gl, and other URL shorteners
- **Suspicious TLDs:** `.xyz`, `.top`, `.click`, `.link`, `.info`, `.tk`

### 4. Fee/Payment Pressure Detection (UAE-Relevant)

Specialized detection for regional delivery and payment scams:

- **Currency Detection:** AED, DHS, Dirham references
- **Fee Keywords:** "re-delivery fee", "customs charge", "processing fee"
- **Small Amount Patterns:** Low-value amounts designed to seem legitimate

### 5. User-Friendly Output

Structured JSON response with complete analysis:

| Field | Type | Description |
|-------|------|-------------|
| `risk_score` | int | Risk score from 0 (safe) to 100 (definite phishing) |
| `label` | string | Classification: "Safe", "Suspicious", or "Phishing" |
| `confidence` | string | Confidence level: "Low", "Medium", or "High" |
| `reasons` | array | Human-readable list explaining each detected risk factor |
| `urls` | array | All URLs extracted from the image |
| `extracted_text` | string | Complete OCR text output |
| `extracted_text_preview` | string | First 400 characters of extracted text |

---

## Installation

### Prerequisites

1. **Python 3.9+** – Required for all dependencies
2. **Tesseract OCR** – Must be installed separately (see below)

### Install Tesseract OCR

#### Windows

1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer and install to: `C:\Program Files\Tesseract-OCR\`
3. Add to system PATH:
   - Open System Properties → Advanced → Environment Variables
   - Add `C:\Program Files\Tesseract-OCR\` to the `Path` variable
4. Verify installation:
   ```cmd
   tesseract --version
   ```

#### macOS

```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install tesseract-ocr
```

#### Linux (Fedora/RHEL)

```bash
sudo dnf install tesseract
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
phishnet-ocr-detector/
├── src/
│   ├── ocr.py              # OCR text extraction using Tesseract
│   ├── extract.py          # Text extraction utilities
│   ├── rules.py            # Phishing pattern detection rules
│   ├── scoring.py          # Risk score calculation logic
│   └── pipeline.py         # Main analysis pipeline (entry point)
├── test_images/
│   ├── phish_chat.png                  # Sample phishing chat screenshot
│   ├── phish_chat_simulated.png        # Simulated phishing chat
│   ├── phish_linkedin.png              # LinkedIn phishing example
│   ├── phish_delivery_simulated.png    # Delivery scam simulation
│   ├── phish_account_alert_simulated.png  # Account alert phishing
│   └── safe_message.png                # Safe message for comparison
├── app.py                  # Streamlit web interface
├── requirements.txt        # Python dependencies
├── DESIGN.md               # Technical design documentation
└── README.md               # This file
```

---

## Usage

### Option 1: Python API

```python
from src.pipeline import analyze_image_path

# Analyze an image file
result = analyze_image_path("test_images/phish_chat.png")

# Access results
print(f"Risk Score: {result['risk_score']}/100")
print(f"Label: {result['label']}")
print(f"Confidence: {result['confidence']}")
print(f"Reasons: {result['reasons']}")
print(f"URLs Found: {result['urls']}")
print(f"Extracted Text: {result['extracted_text_preview']}")
```

### Option 2: Streamlit Web App

Launch the interactive web interface:

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser to:
- Upload images for analysis
- View real-time phishing detection results
- Explore detected patterns and risk factors

### Option 3: Command Line Interface

Run the pipeline directly from the command line:

```bash
python -m src.pipeline
```

This will process test images and display analysis results in the terminal.

---

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
    "Suspicious keyword in path: verify",
    "Multiple hyphens in domain (2)"
  ],
  "urls": [
    "uae-post-track.com/verify"
  ],
  "extracted_text": "Emirates Post: Your parcel is on hold due to unpaid shipping fee. Pay AED 7.50 to confirm your details and reschedule delivery. Visit: uae-post-track.com/verify. Failure to pay within 24 hours will result in your parcel being cancelled.",
  "extracted_text_preview": "Emirates Post: Your parcel is on hold due to unpaid shipping fee. Pay AED 7.50 to confirm your details and reschedule delivery..."
}
```

---

## Backend Integration

### API Usage

For integration with the PhishNet backend system:

```python
from src.pipeline import analyze_image, analyze_image_path
from PIL import Image

# Method 1: Analyze from file path
result = analyze_image_path("path/to/screenshot.png")

# Method 2: Analyze from PIL Image object
image = Image.open("path/to/screenshot.png")
result = analyze_image(image)

# Method 3: Analyze from bytes (useful for API endpoints)
with open("path/to/screenshot.png", "rb") as f:
    image_bytes = f.read()
image = Image.open(io.BytesIO(image_bytes))
result = analyze_image(image)
```

### Response Format

| Field | Type | Description |
|-------|------|-------------|
| `risk_score` | `int` | Risk score from 0 to 100 |
| `label` | `str` | "Safe" (0-39), "Suspicious" (40-69), or "Phishing" (70-100) |
| `confidence` | `str` | "Low", "Medium", or "High" based on evidence strength |
| `reasons` | `list[str]` | Array of human-readable explanations for the score |
| `urls` | `list[str]` | All URLs extracted from the image |
| `extracted_text` | `str` | Complete text extracted via OCR |
| `extracted_text_preview` | `str` | Truncated preview (first 400 characters) |

### Integration Example

```python
import json
from src.pipeline import analyze_image_path

def check_image_for_phishing(image_path: str) -> dict:
    """
    Wrapper function for backend integration.
    Returns structured response for API consumers.
    """
    result = analyze_image_path(image_path)
    
    return {
        "is_phishing": result["label"] == "Phishing",
        "is_suspicious": result["label"] in ["Phishing", "Suspicious"],
        "risk_score": result["risk_score"],
        "confidence": result["confidence"],
        "reasons": result["reasons"],
        "urls_detected": result["urls"],
        "text_preview": result["extracted_text_preview"]
    }
```

---

## Testing

### Run Full Test Suite

Execute the pipeline against all test images:

```bash
python -m src.pipeline
```

### Test Individual Images

```python
from src.pipeline import analyze_image_path
import json

# Test a specific image
result = analyze_image_path("test_images/phish_linkedin.png")
print(json.dumps(result, indent=2))
```

### Test All Sample Images

```python
from src.pipeline import analyze_image_path
import os
import json

test_dir = "test_images"
for filename in os.listdir(test_dir):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        filepath = os.path.join(test_dir, filename)
        result = analyze_image_path(filepath)
        print(f"\n{'='*50}")
        print(f"File: {filename}")
        print(f"Score: {result['risk_score']}/100 ({result['label']})")
        print(f"Reasons: {', '.join(result['reasons'][:3])}...")
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `pytesseract` | Python wrapper for Tesseract OCR engine |
| `Pillow` | Image loading and preprocessing |
| `streamlit` | Interactive web interface |
| `numpy` | Numerical operations for image processing |
| `opencv-python` | Advanced image preprocessing for OCR optimization |

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## Notes

- **Tesseract Installation:** Tesseract OCR must be installed separately and accessible via PATH. The Python `pytesseract` package is only a wrapper.

- **Windows PATH Configuration:** If Tesseract is not in PATH, you can set the path directly in `src/ocr.py`:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

- **Image Quality:** For optimal OCR results, use clear, high-resolution screenshots with good contrast. Blurry or low-quality images may produce incomplete text extraction.

- **False Positives:** The system uses conservative thresholds. Legitimate messages with urgency language may occasionally be flagged as suspicious—always review the `reasons` array for context.

- **Regional Customization:** The fee/payment detection is optimized for UAE-specific scams (AED/DHS currency). Additional regional patterns can be added to `src/rules.py`.

---

## Author

**Sanaullah Bilal Syed** (7598063)  
Member 3 – Image Phishing Detection  
PhishNet Project
