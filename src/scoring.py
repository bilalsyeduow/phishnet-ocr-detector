"""
Scoring module for calculating phishing risk scores from features.
"""

from typing import Tuple

# Feature weights for risk scoring
FEATURE_WEIGHTS = {
    "urgency": 15,
    "credential_request": 25,
    "brand_mention": 10,
    "threat_language": 15,
    "reward_bait": 15,
    "grammar_issues": 10,
    "has_url": 10,
    "fee_bait": 10,
}

# Risk level thresholds
THRESHOLDS = {
    "high": 60,
    "medium": 30,
}


def score_risk(features: dict) -> Tuple[int, str, str]:
    """
    Calculate risk score from feature flags.
    
    Args:
        features: Dictionary of boolean feature flags from analyze_text.
    
    Returns:
        Tuple of (risk_score, label, confidence)
        - risk_score: Integer 0-100
        - label: "Phishing", "Suspicious", or "Safe"
        - confidence: "High", "Medium", or "Low"
    """
    # Calculate raw score
    score = 0
    active_features = 0
    
    for feature, weight in FEATURE_WEIGHTS.items():
        if features.get(feature, False):
            score += weight
            active_features += 1
    
    # Add url_bonus directly (can be positive or negative)
    score += features.get("url_bonus", 0)
    
    # Clamp to 0-100
    score = max(0, min(score, 100))
    
    # Determine label based on thresholds
    if score >= THRESHOLDS["high"]:
        label = "Phishing"
    elif score >= THRESHOLDS["medium"]:
        label = "Suspicious"
    else:
        label = "Safe"
    
    # Determine confidence based on both score and active features
    # High: strong score with multiple indicators, or very high score
    # Medium: moderate score with some indicators
    # Low: weak evidence overall
    if (score >= THRESHOLDS["high"] and active_features >= 3) or score >= 80:
        confidence = "High"
    elif (score >= THRESHOLDS["medium"] and active_features >= 2) or active_features >= 3:
        confidence = "Medium"
    else:
        confidence = "Low"
    
    return score, label, confidence


if __name__ == "__main__":
    # Test cases
    test_features = [
        # High risk
        {
            "urgency": True,
            "credential_request": True,
            "brand_mention": True,
            "threat_language": True,
            "reward_bait": False,
            "grammar_issues": True,
            "has_url": True,
        },
        # Medium risk
        {
            "urgency": True,
            "credential_request": False,
            "brand_mention": True,
            "threat_language": False,
            "reward_bait": False,
            "grammar_issues": False,
            "has_url": True,
        },
        # Low risk
        {
            "urgency": False,
            "credential_request": False,
            "brand_mention": False,
            "threat_language": False,
            "reward_bait": False,
            "grammar_issues": False,
            "has_url": False,
        },
    ]
    
    for i, features in enumerate(test_features, 1):
        score, label, confidence = score_risk(features)
        print(f"Test {i}: Score={score}, Label={label}, Confidence={confidence}")
