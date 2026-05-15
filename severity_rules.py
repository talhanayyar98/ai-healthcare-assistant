import json
import re


SEVERE_KEYWORDS = [
    "chest pain",
    "shortness of breath",
    "difficulty breathing",
    "fainting",
    "seizure",
    "heavy bleeding",
    "severe allergic reaction",
    "face drooping",
    "slurred speech",
]

MODERATE_KEYWORDS = [
    "fever",
    "persistent cough",
    "vomiting",
    "diarrhea",
    "rash",
    "swelling",
    "infection",
    "ear pain",
    "sore throat",
]

MINOR_REMEDIES = {
    "cough": ["Warm fluids", "Honey if appropriate", "Rest"],
    "sore throat": ["Warm salt-water gargle", "Warm fluids", "Rest"],
    "cold": ["Warm fluids", "Rest", "Monitor fever"],
    "rash": ["Keep the area clean", "Avoid scratching", "Monitor spreading"],
    "small cut": ["Wash with clean water", "Apply light bandage", "Watch for infection"],
}


def try_parse_json_block(raw_text: str):
    if not raw_text:
        return None

    match = re.search(r"\{.*\}", raw_text.strip(), flags=re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def build_rule_based_assessment(text: str):
    normalized = (text or "").lower()
    red_flags = [keyword for keyword in SEVERE_KEYWORDS if keyword in normalized]

    if red_flags:
        return {
            "severity": "Severe",
            "urgency": "emergency",
            "possible_conditions": [
                "Possible emergency warning signs",
                "Condition cannot be safely assessed by prototype alone",
            ],
            "recommendation": (
                "Seek urgent medical attention immediately or contact emergency services."
            ),
            "home_remedies": [],
            "red_flags": red_flags,
            "follow_up": "Do not rely on this prototype alone for severe symptoms.",
        }

    matched_moderate = [keyword for keyword in MODERATE_KEYWORDS if keyword in normalized]
    if matched_moderate:
        return {
            "severity": "Moderate",
            "urgency": "doctor_soon",
            "possible_conditions": [
                "Common infection or inflammation",
                "Minor illness that may need monitoring",
            ],
            "recommendation": (
                "Monitor symptoms closely. If they worsen, last several days, or include "
                "new severe signs, contact a clinician."
            ),
            "home_remedies": _pick_home_remedies(normalized),
            "red_flags": matched_moderate,
            "follow_up": "Arrange a medical review if symptoms persist or get worse.",
        }

    return {
        "severity": "Mild",
        "urgency": "home_care",
        "possible_conditions": [
            "Minor self-limiting issue",
            "Symptom description too limited for stronger assessment",
        ],
        "recommendation": "Home care and monitoring may be enough if symptoms stay mild.",
        "home_remedies": _pick_home_remedies(normalized),
        "red_flags": [],
        "follow_up": "Seek medical advice if symptoms worsen or do not improve.",
    }


def _pick_home_remedies(normalized_text: str):
    for keyword, remedies in MINOR_REMEDIES.items():
        if keyword in normalized_text:
            return remedies
    return ["Rest", "Drink enough fluids", "Monitor symptoms"]
