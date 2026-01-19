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
    
    # Cap at 100
    score = min(score, 100)
    
    # Determine label based on thresholds
    if score >= THRESHOLDS["high"]:
        label = "Phishing"
    elif score >= THRESHOLDS["medium"]:
        label = "Suspicious"
    else:
        label = "Safe"
    
    # Determine confidence based on number of active features
    if active_features >= 4:
        confidence = "High"
    elif active_features >= 2:
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
