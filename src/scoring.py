"""Scoring module for calculating phishing risk scores from features."""

from typing import Tuple

FEATURE_WEIGHTS = {
    "urgency": 15, "credential_request": 25, "brand_mention": 10,
    "threat_language": 15, "reward_bait": 15, "grammar_issues": 10,
    "has_url": 10, "fee_bait": 10,
}

THRESHOLDS = {"high": 60, "medium": 30}


def score_risk(features: dict) -> Tuple[int, str, str]:
    """Calculate risk score from feature flags, returns (score, label, confidence)."""
    score = 0
    active_features = 0
    
    for feature, weight in FEATURE_WEIGHTS.items():
        if features.get(feature, False):
            score += weight
            active_features += 1
    
    score += features.get("url_bonus", 0)
    
    score = max(0, min(score, 100))
    
    if score >= THRESHOLDS["high"]:
        label = "Phishing"
    elif score >= THRESHOLDS["medium"]:
        label = "Suspicious"
    else:
        label = "Safe"
    
    # confidence based on score + how many indicators fired
    if (score >= THRESHOLDS["high"] and active_features >= 3) or score >= 80:
        confidence = "High"
    elif (score >= THRESHOLDS["medium"] and active_features >= 2) or active_features >= 3:
        confidence = "Medium"
    else:
        confidence = "Low"
    
    return score, label, confidence
