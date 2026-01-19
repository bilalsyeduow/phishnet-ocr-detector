```md
# Design – OCR-Based Image Phishing Detector (Member 3)

## Goal
Detect phishing attempts embedded inside images/screenshots by:
1) Extracting text and URLs from an image (OCR)
2) Identifying modern phishing intent patterns (rule-based signals)
3) Producing an explainable risk score (0–100) and user-friendly warning

This module is designed to plug into PhishNet as an independent detection pillar.

---

## System Overview

### Input
- Screenshot / image (PNG/JPG)
Examples:
- delivery scam chats
- fake bank alerts
- “support” impersonation chats
- invoice/payment request screenshots

### Output
- `risk_score`: 0–100
- `label`: Safe / Suspicious / Phishing
- `confidence`: Low / Medium / High
- `reasons`: list of human-readable explanations
- `urls`: extracted URLs/domains from OCR text
- `extracted_text` + `extracted_text_preview`

---

## Pipeline Stages

### Stage 1 — OCR Text Extraction
**Responsibility:** convert image → raw text

- Preprocessing may include:
  - grayscale
  - thresholding/denoise (optional)
- OCR engine:
  - Tesseract (local)
  - Output is a single text string

**Failure handling:**
- If OCR fails or returns empty text:
  - return low score + reason like “No readable text found.”

---

### Stage 2 — Text Normalization
Normalize before analysis:
- lowercase for matching
- clean repeated whitespace
- basic OCR fixes (optional), e.g. `wi.` → `www.`

---

### Stage 3 — Feature Detection (Rule-Based Signals)
This stage produces a `features` dictionary and reasons.

Signals (examples):
- **Urgency**: “within 2 hours”, “on hold”, “act now”
- **Credential/Identity Requests**: “confirm your details”, “password”, “OTP”
- **Brand Impersonation**: known brand names in suspicious context
- **Threat Language**: “will be cancelled”, “suspended”, “terminated”
- **Reward Bait**: “you won”, “free gift”
- **Fee/Payment Pressure**: currency + fee/payment words (AED/DHS + fee)
- **URL Presence**: detects URLs/domains in OCR text

---

### Stage 4 — URL Plausibility Heuristics
Modern phishing often uses believable but suspicious URLs.

Heuristics:
- suspicious path keywords: `/verify`, `/login`, `/update`, `/confirm`
- multiple hyphens in domain
- shortened links (optional list)
- suspicious TLDs (optional list)

These heuristics add:
- extra reasons for explainability
- optional small score bonus (capped) to prevent domination

---

### Stage 5 — Risk Scoring
A weighted scoring model produces `risk_score` 0–100.

Example approach:
- base score from triggered features (weights)
- + small capped bonus from URL heuristics (modern phishing)
- clamp score to 0–100

Labels:
- 0–30: Safe
- 31–60: Suspicious
- 61–100: Phishing

Confidence:
- derived from score bands (e.g., High if >= 70)

---

### Stage 6 — UI Presentation
Dashboard shows:
- color-coded status (green/yellow/red styling)
- risk score + label + confidence
- reasons and extracted URLs
- extracted text preview

This supports layman users who won’t interpret numeric scores alone.

---

## Integration with PhishNet (Backend)
Expose a single call:

`analyze_image_path(image_path: str) -> dict`

The backend orchestrator:
1) receives image upload
2) saves to temporary file
3) calls `analyze_image_path`
4) returns JSON to frontend

---

## Threat Model Alignment (Modern Phishing)
The detector focuses on modern scam patterns:
- screenshot-based phishing via messaging platforms
- impersonation of delivery/bank services
- urgency + small-fee pressure (UAE-relevant)
- embedded URLs with verification/login paths

---

## Limitations
- OCR errors for low-quality images (blur, small fonts)
- rule-based approach can miss novel phrasing
- no real-time threat intel / reputation APIs (offline design)

---

## Future Enhancements (Optional)
- multi-screenshot conversation aggregation
- typosquat/homoglyph detection for domains/brands
- allowlists for known official domains
- lightweight ML classifier on extracted text (optional)
