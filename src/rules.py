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

# Common OCR errors in URLs (order matters - longer patterns first)
OCR_URL_FIXES = [
    ("wwvv.", "www."),
    ("vvww.", "www."),
    ("vvvvw.", "www."),
    ("wi.", "www."),   # Common OCR misread
    ("ww.", "www."),   # Missing 'w'
    ("htpps://", "https://"),
    ("htrps://", "https://"),
    ("hnps://", "https://"),
    ("htpp://", "http://"),
]

# Short brand names that need word boundary matching
SHORT_BRANDS = {"du", "rta", "fab", "moi", "dhl"}

# Grammar/slang indicators
SLANG_PATTERNS = [
    "ur", "u r", "acc", "acct", "plz", "pls", "dont", "wont", "cant",
    "asap", "b4", "2day", "4u", "cuz", "bcuz", "thru"
]


import re
from typing import Optional


def _fix_ocr_urls(text: str) -> str:
    """Fix common OCR errors in URLs."""
    fixed = text
    for wrong, correct in OCR_URL_FIXES:
        # Use word boundary to avoid replacing within already-correct URLs
        # e.g., don't match 'ww.' inside 'www.'
        pattern = rf'(?<![a-zA-Z]){re.escape(wrong)}'
        fixed = re.sub(pattern, correct, fixed, flags=re.IGNORECASE)
    return fixed


def _extract_urls(text: str) -> list[str]:
    """Extract URLs and domains from text."""
    fixed_text = _fix_ocr_urls(text)
    
    # Pattern for full URLs (http/https or www.)
    url_pattern = r'https?://[^\s<>"\')\]]+|www\.[^\s<>"\')\]]+'
    # Pattern for domain-like strings with proper TLD (e.g., example.com, bit.ly/xxx)
    # Requires a recognizable TLD pattern
    domain_pattern = r'\b[a-zA-Z0-9][-a-zA-Z0-9]*(?:\.[a-zA-Z0-9][-a-zA-Z0-9]*)*\.(?:com|net|org|io|ly|co|me|info|biz|ae|uk|de|fr|ru|cn|xyz|online|site|app|dev)(?:/[^\s<>"\')\]]*)?'
    
    urls = []
    
    # Find full URLs first (higher priority)
    for match in re.findall(url_pattern, fixed_text, re.IGNORECASE):
        cleaned = match.rstrip('.,;:')
        if cleaned not in urls:
            urls.append(cleaned)
    
    # Find domain patterns
    for match in re.findall(domain_pattern, fixed_text, re.IGNORECASE):
        cleaned = match.rstrip('.,;:')
        # Skip if it's already a substring of an existing URL
        if not any(cleaned in existing_url for existing_url in urls):
            if cleaned not in urls:
                urls.append(cleaned)
    
    return urls


def _find_matches(text: str, keywords: list[str], use_word_boundary: bool = False) -> list[str]:
    """Find keywords that match in text (case-insensitive).
    
    Args:
        text: Text to search in
        keywords: List of keywords to find
        use_word_boundary: If True, use word boundaries for short keywords
    """
    text_lower = text.lower()
    matches = []
    for kw in keywords:
        kw_lower = kw.lower()
        # Use word boundary for short keywords to avoid false positives
        if use_word_boundary and kw_lower in SHORT_BRANDS:
            pattern = rf'\b{re.escape(kw_lower)}\b'
            if re.search(pattern, text_lower):
                matches.append(kw)
        elif kw_lower in text_lower:
            matches.append(kw)
    return matches


def _check_grammar_issues(text: str) -> tuple[bool, list[str]]:
    """Check for grammar issues: excessive punctuation, ALL CAPS, slang."""
    issues = []
    
    # Check for excessive exclamation marks
    exclamation_count = text.count('!')
    if exclamation_count >= 3:
        issues.append(f"excessive exclamation marks ({exclamation_count})")
    
    # Check for ALL CAPS words (at least 4 chars to avoid acronyms)
    words = re.findall(r'\b[A-Z]{4,}\b', text)
    caps_words = [w for w in words if not w.isdigit()]
    if len(caps_words) >= 2:
        issues.append(f"ALL CAPS words: {', '.join(caps_words[:3])}")
    
    # Check for slang patterns
    text_lower = text.lower()
    found_slang = []
    for slang in SLANG_PATTERNS:
        # Use word boundary check for short patterns
        pattern = rf'\b{re.escape(slang)}\b'
        if re.search(pattern, text_lower):
            found_slang.append(slang)
    
    if found_slang:
        issues.append(f"informal language: {', '.join(found_slang[:3])}")
    
    return len(issues) > 0, issues


def analyze_text(
    text: str,
    urls: Optional[list[str]] = None
) -> tuple[dict, list[str], list[str]]:
    """
    Analyze text for phishing indicators.
    
    Args:
        text: The text content to analyze (e.g., from OCR)
        urls: Optional list of URLs. If None, extracts from text.
    
    Returns:
        Tuple of (features_dict, reasons_list, urls_list)
        - features: dict with boolean flags for each indicator
        - reasons: list of human-readable reasons with matched keywords
        - urls: list of URLs found or provided
    """
    reasons = []
    
    # Extract or use provided URLs
    extracted_urls = urls if urls is not None else _extract_urls(text)
    
    # Check urgency
    urgency_matches = _find_matches(text, URGENCY)
    has_urgency = len(urgency_matches) > 0
    if has_urgency:
        top_matches = urgency_matches[:3]
        reasons.append(f"Urgency language: {', '.join(top_matches)}")
    
    # Check credential requests
    credential_matches = _find_matches(text, CREDENTIAL)
    has_credential = len(credential_matches) > 0
    if has_credential:
        top_matches = credential_matches[:3]
        reasons.append(f"Credential request: {', '.join(top_matches)}")
    
    # Check brand mentions (use word boundary for short names like "du")
    brand_matches = _find_matches(text, BRANDS_UAE, use_word_boundary=True)
    has_brand = len(brand_matches) > 0
    if has_brand:
        top_matches = brand_matches[:2]
        reasons.append(f"Brand mentioned: {', '.join(top_matches)}")
    
    # Check threat language
    threat_matches = _find_matches(text, THREATS)
    has_threat = len(threat_matches) > 0
    if has_threat:
        top_matches = threat_matches[:2]
        reasons.append(f"Threat language: {', '.join(top_matches)}")
    
    # Check reward bait
    reward_matches = _find_matches(text, REWARDS)
    has_reward = len(reward_matches) > 0
    if has_reward:
        top_matches = reward_matches[:2]
        reasons.append(f"Reward/prize bait: {', '.join(top_matches)}")
    
    # Check grammar issues
    has_grammar, grammar_reasons = _check_grammar_issues(text)
    if has_grammar:
        reasons.append(f"Grammar issues: {'; '.join(grammar_reasons[:2])}")
    
    # Check for URLs
    has_url = len(extracted_urls) > 0
    if has_url:
        reasons.append(f"Contains URL(s): {', '.join(extracted_urls[:2])}")
    
    features = {
        "urgency": has_urgency,
        "credential_request": has_credential,
        "brand_mention": has_brand,
        "threat_language": has_threat,
        "reward_bait": has_reward,
        "grammar_issues": has_grammar,
        "has_url": has_url,
    }
    
    return features, reasons, extracted_urls


if __name__ == "__main__":
    # Test cases
    test_texts = [
        # Phishing-like message
        """URGENT! Your Emirates NBD account has been suspended!
        Verify ur acc immediately or it will be terminated.
        Click here: wi.emirates-nbd-secure.com/verify
        Act now to avoid losing access!!!""",
        
        # Reward scam
        """Congratulations! You've won a FREE iPhone 14!
        Claim your prize now at bit.ly/free-prize
        Enter ur credit card for shipping only.""",
        
        # Clean text
        """Hello, this is a reminder about your scheduled appointment
        tomorrow at 2pm. Please let us know if you need to reschedule.""",
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}:")
        print(f"{'='*60}")
        print(f"Text preview: {text[:80]}...")
        
        features, reasons, urls = analyze_text(text)
        
        print(f"\nFeatures: {features}")
        print(f"\nReasons ({len(reasons)}):")
        for reason in reasons:
            print(f"  - {reason}")
        print(f"\nURLs found: {urls}")
