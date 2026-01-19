# phishnet-ocr-detector
# PhishNet – OCR-Based Image Phishing Detector (sanaullah bilal syed- 7598063)

This module detects **modern phishing scams embedded in screenshots/images** (e.g., WhatsApp/Telegram delivery scams, bank alerts, fake support chats).  
It extracts text using OCR, analyzes phishing intent patterns, evaluates URL plausibility, and outputs an **explainable risk assessment** (score + reasons + URLs).

## What this solves (Modern Phishing)
Modern phishing often arrives as:
- **Screenshots** shared in chat apps (bypasses email/text filters)
- **Realistic language** (sometimes AI-written) with subtle urgency/pressure
- **Small-fee delivery scams** (e.g., “pay AED 7.50 re-delivery fee”)
- **Look-alike URLs** with “verify/login/update” paths

This module focuses on these patterns rather than only obvious spam.

---

## Features
### 1) OCR Text Extraction
- Input: screenshot/image (PNG/JPG)
- Output: extracted text + preview

### 2) Explainable Phishing Analysis (Rule-Based)
Detects:
- Urgency language (time pressure)
- Credential/identity requests (“confirm details”, “password”, etc.)
- Brand impersonation (e.g., Emirates Post / banks)
- Threat language (“will be cancelled”, “suspended”)
- Reward bait (“you won”)
- Grammar/format anomalies (optional)
- URL presence + URL plausibility signals

### 3) URL Plausibility Heuristics (Modern Phishing)
Flags suspicious URL structure:
- suspicious path keywords (verify/login/update/confirm)
- multiple hyphens in domain
- shortened links (if configured)
- suspicious TLDs (if configured)

### 4) Fee/Payment Pressure Detection (UAE-relevant)
Detects small-fee pressure scams:
- currency cues (AED/DHS/dirham) + fee/payment words

### 5) User-Friendly Output
- risk_score (0–100)
- label (Safe / Suspicious / Phishing)
- confidence (Low/Medium/High)
- reasons (bullet list)
- urls (extracted)
- extracted_text + preview

---Tesseract OCR engine must be installed separately and added to PATH (or set in code as pytesseract.pytesseract.tesseract_cmd).
Author: Sanaullah Bilal Syed (Member 3 – Image Phishing Detection)
---

