URGENCY = [
    "urgent", "immediately", "act now", "within 24 hours", "expires today",
    "account suspended", "locked", "on hold", "verify now", "last warning"
]

CREDENTIAL = [
    "password", "otp", "verification code", "login", "sign in", "cvv",
    "credit card", "debit card", "bank", "confirm your details", "update payment"
]

BRANDS_UAE = [
    "emirates post", "aramex", "dhl", "fedex", "amazon", "microsoft", "apple",
    "paypal", "netflix", "enbd", "emirates nbd", "adcb", "fab", "etisalat",
    "du", "rta", "dubai police", "moi"
]

THREATS = [
    "unauthorized", "suspicious activity", "will be terminated", "legal action",
    "account will be closed", "will be cancelled", "fine", "penalty"
]

REWARDS = [
    "you've won", "won", "prize", "free gift", "claim your prize",
    "selected winner", "congratulations"
]

OCR_URL_FIXES = [
    ("wwvv.", "www."), ("vvww.", "www."), ("vvvvw.", "www."), ("wi.", "www."),
    ("ww.", "www."), ("htpps://", "https://"), ("htrps://", "https://"),
    ("hnps://", "https://"), ("htpp://", "http://"),
]

SHORT_BRANDS = {"du", "rta", "fab", "moi", "dhl"}

SLANG_PATTERNS = [
    "ur", "u r", "acc", "acct", "plz", "pls", "dont", "wont", "cant",
    "asap", "b4", "2day", "4u", "cuz", "bcuz", "thru"
]

URL_PATH_KEYWORDS = [
    "verify", "login", "update", "confirm", "secure", "account", "payment", "unlock"
]

SUSPICIOUS_TLDS = [".xyz", ".top", ".site", ".click", ".icu", ".monster", ".zip", ".mov"]

SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "cutt.ly", "rebrand.ly", "is.gd", "rb.gy"]

FEE_WORDS = [
    "fee", "payment", "pay", "charged", "charge", "re-delivery", "redelivery",
    "delivery fee", "small fee", "amount", "invoice"
]

CURRENCY_WORDS = ["aed", "dhs", "dirham", "dirhams", "aed.", "aed ", "dh", "dhs "]


import re
from typing import Optional
from urllib.parse import urlparse


def _fix_ocr_urls(text):
    """Fix common OCR errors in URLs."""
    fixed = text
    
    # handles cases where OCR adds spaces after www prefix
    space_fixes = [
        (r'(?<![a-zA-Z])vvww\.\s+', 'www.'),
        (r'(?<![a-zA-Z])wwvv\.\s+', 'www.'),
        (r'(?<![a-zA-Z])vvvvw\.\s+', 'www.'),
        (r'(?<![a-zA-Z])www\.\s+', 'www.'),
        (r'(?<![a-zA-Z])ww\.\s+', 'www.'),
        (r'(?<![a-zA-Z])wi\.\s+', 'www.'),
        (r'(?<![a-zA-Z])w\.\s+', 'www.'),
    ]
    for pattern, replacement in space_fixes:
        fixed = re.sub(pattern, replacement, fixed, flags=re.IGNORECASE)
    
    for wrong, correct in OCR_URL_FIXES:
        pattern = rf'(?<![a-zA-Z]){re.escape(wrong)}'
        fixed = re.sub(pattern, correct, fixed, flags=re.IGNORECASE)
    return fixed


def _extract_urls(text):
    """Extract URLs and domains from text."""
    fixed_text = _fix_ocr_urls(text)
    
    url_pattern = r'https?://[^\s<>"\')\]]+|www\.[^\s<>"\')\]]+'
    domain_pattern = r'\b[a-zA-Z0-9][-a-zA-Z0-9]*(?:\.[a-zA-Z0-9][-a-zA-Z0-9]*)*\.(?:com|net|org|io|ly|co|me|info|biz|ae|uk|de|fr|ru|cn|xyz|online|site|app|dev)(?:/[^\s<>"\')\]]*)?'
    
    urls = []
    
    for match in re.findall(url_pattern, fixed_text, re.IGNORECASE):
        cleaned = match.rstrip('.,;:')
        if cleaned not in urls:
            urls.append(cleaned)
    
    for match in re.findall(domain_pattern, fixed_text, re.IGNORECASE):
        cleaned = match.rstrip('.,;:')
        if not any(cleaned in existing_url for existing_url in urls):
            if cleaned not in urls:
                urls.append(cleaned)
    
    return urls


def _find_matches(text, keywords, use_word_boundary=False):
    """Find keywords that match in text (case-insensitive)."""
    text_lower = text.lower()
    matches = []
    for kw in keywords:
        kw_lower = kw.lower()
        if use_word_boundary and kw_lower in SHORT_BRANDS:
            pattern = rf'\b{re.escape(kw_lower)}\b'
            if re.search(pattern, text_lower):
                matches.append(kw)
        elif kw_lower in text_lower:
            matches.append(kw)
    return matches


def _check_grammar_issues(text):
    """Check for grammar issues: excessive punctuation, ALL CAPS, slang."""
    issues = []
    
    exclamation_count = text.count('!')
    if exclamation_count >= 3:
        issues.append(f"excessive exclamation marks ({exclamation_count})")
    
    # 4+ chars to avoid matching acronyms like "USA"
    words = re.findall(r'\b[A-Z]{4,}\b', text)
    caps_words = [w for w in words if not w.isdigit()]
    if len(caps_words) >= 2:
        issues.append(f"ALL CAPS words: {', '.join(caps_words[:3])}")
    
    text_lower = text.lower()
    found_slang = []
    for slang in SLANG_PATTERNS:
        pattern = rf'\b{re.escape(slang)}\b'
        if re.search(pattern, text_lower):
            found_slang.append(slang)
    
    if found_slang:
        issues.append(f"informal language: {', '.join(found_slang[:3])}")
    
    return len(issues) > 0, issues


def _normalize_url_candidate(u):
    """Strip punctuation and fix common OCR errors in URLs."""
    cleaned = u.rstrip('.,;:!?')
    
    space_fixes = [
        (r'(?<![a-zA-Z])vvww\.\s+', 'www.'),
        (r'(?<![a-zA-Z])wwvv\.\s+', 'www.'),
        (r'(?<![a-zA-Z])vvvvw\.\s+', 'www.'),
        (r'(?<![a-zA-Z])www\.\s+', 'www.'),
        (r'(?<![a-zA-Z])ww\.\s+', 'www.'),
        (r'(?<![a-zA-Z])wi\.\s+', 'www.'),
        (r'(?<![a-zA-Z])w\.\s+', 'www.'),
    ]
    for pattern, replacement in space_fixes:
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
    
    for wrong, correct in OCR_URL_FIXES:
        pattern = rf'(?<![a-zA-Z]){re.escape(wrong)}'
        cleaned = re.sub(pattern, correct, cleaned, flags=re.IGNORECASE)
    return cleaned


def _get_domain_and_path(u):
    """Parse URL to extract domain and path."""
    url = u.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    return domain, path


def url_risk_reasons(urls: list[str], brands: list[str]) -> tuple[int, list[str]]:
    """Analyze URLs for phishing risk indicators, returns (score, reasons)."""
    extra_score = 0
    reasons = []

    for url in urls:
        normalized = _normalize_url_candidate(url)
        domain, path = _get_domain_and_path(normalized)

        for shortener in SHORTENERS:
            if domain == shortener or domain.endswith('.' + shortener):
                extra_score += 15
                reasons.append(f"Shortened link detected: {shortener}")
                break

        for tld in SUSPICIOUS_TLDS:
            if domain.endswith(tld):
                extra_score += 10
                reasons.append(f"Suspicious TLD: {tld}")
                break

        for keyword in URL_PATH_KEYWORDS:
            if keyword in path:
                extra_score += 10
                reasons.append(f"Suspicious keyword in path: {keyword}")
                break

        for brand in brands:
            brand_lower = brand.lower().replace(' ', '')
            if brand_lower in domain and '-' in domain:
                extra_score += 10
                reasons.append(f"Possible brand impersonation: {brand} with hyphens")
                break

        hyphen_count = domain.count('-')
        if hyphen_count >= 2:
            extra_score += 5
            reasons.append(f"Multiple hyphens in domain ({hyphen_count})")

        if len(domain) >= 28:
            extra_score += 5
            reasons.append(f"Unusually long domain ({len(domain)} chars)")

    capped_score = min(extra_score, 25)  # cap seems to work well

    return capped_score, reasons


def analyze_text(
    text: str,
    urls: Optional[list[str]] = None
) -> tuple[dict, list[str], list[str]]:
    """Analyze text for phishing indicators, returns (features, reasons, urls)."""
    reasons = []
    
    extracted_urls = urls if urls is not None else _extract_urls(text)
    
    urgency_matches = _find_matches(text, URGENCY)
    has_urgency = len(urgency_matches) > 0
    if has_urgency:
        top_matches = urgency_matches[:3]
        reasons.append(f"Urgency language: {', '.join(top_matches)}")
    
    credential_matches = _find_matches(text, CREDENTIAL)
    has_credential = len(credential_matches) > 0
    if has_credential:
        top_matches = credential_matches[:3]
        reasons.append(f"Credential request: {', '.join(top_matches)}")
    
    brand_matches = _find_matches(text, BRANDS_UAE, use_word_boundary=True)
    has_brand = len(brand_matches) > 0
    if has_brand:
        top_matches = brand_matches[:2]
        reasons.append(f"Brand mentioned: {', '.join(top_matches)}")
    
    threat_matches = _find_matches(text, THREATS)
    has_threat = len(threat_matches) > 0
    if has_threat:
        top_matches = threat_matches[:2]
        reasons.append(f"Threat language: {', '.join(top_matches)}")
    
    reward_matches = _find_matches(text, REWARDS)
    has_reward = len(reward_matches) > 0
    if has_reward:
        top_matches = reward_matches[:2]
        reasons.append(f"Reward/prize bait: {', '.join(top_matches)}")
    
    has_grammar, grammar_reasons = _check_grammar_issues(text)
    if has_grammar:
        reasons.append(f"Grammar issues: {'; '.join(grammar_reasons[:2])}")
    
    has_url = len(extracted_urls) > 0
    if has_url:
        reasons.append(f"Contains URL(s): {', '.join(extracted_urls[:2])}")
    
    fee_matches = _find_matches(text, FEE_WORDS)
    currency_matches = _find_matches(text, CURRENCY_WORDS)
    money_pattern = re.search(r'\b\d+\.\d{2}\b', text)
    has_fee_bait = len(fee_matches) > 0 and (len(currency_matches) > 0 or money_pattern is not None)
    if has_fee_bait:
        reasons.append("Fee/payment pressure detected (common delivery scam tactic).")
    
    url_bonus, url_reasons = url_risk_reasons(extracted_urls, BRANDS_UAE)
    url_suspicious = len(url_reasons) > 0
    if url_suspicious:
        reasons.extend(url_reasons)
    
    features = {
        "urgency": has_urgency,
        "credential_request": has_credential,
        "brand_mention": has_brand,
        "threat_language": has_threat,
        "reward_bait": has_reward,
        "grammar_issues": has_grammar,
        "has_url": has_url,
        "fee_bait": has_fee_bait,
        "url_bonus": url_bonus,
        "url_suspicious": url_suspicious,
    }
    
    return features, reasons, extracted_urls
