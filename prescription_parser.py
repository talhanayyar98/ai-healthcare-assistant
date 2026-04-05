import re


def parse_prescription_text(text):
    """
    Basic rule-based parser for prescription text.
    Designed for demo/prototype use.
    """
    if not text or text.strip() == "":
        return {
            "Patient Name": "Not detected",
            "Date": "Not detected",
            "Doctor / Issuer": "Not detected",
            "Likely Medicine": "Not detected",
            "Likely Dosage": "Not detected",
            "Likely Frequency": "Not detected",
            "Refills": "Not detected"
        }

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    full_text = " ".join(lines)

    patient_name = "Not detected"
    date = "Not detected"
    doctor = "Not detected"
    medicine = "Not detected"
    dosage = "Not detected"
    frequency = "Not detected"
    refills = "Not detected"

    patient_match = re.search(r"Patient Name[:\s]+([A-Za-z ]+)", full_text, re.IGNORECASE)
    if patient_match:
        patient_name = patient_match.group(1).strip()

    date_match = re.search(r"Date[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})", full_text, re.IGNORECASE)
    if date_match:
        date = date_match.group(1).strip()

    doctor_match = re.search(r"(Dr\.?\s+[A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+)", full_text)
    if doctor_match:
        doctor = doctor_match.group(1).strip()

    medicine_match = re.search(
        r"([A-Z][a-zA-Z]+(?:\s+[A-Z]?[a-zA-Z]+)?\s+\d+\s*mg(?:\s+\w+)?)",
        full_text,
        re.IGNORECASE
    )
    if medicine_match:
        medicine = medicine_match.group(1).strip()

    dosage_match = re.search(
        r"(Take\s+.*?)(?:Refills:|#\d+|$)",
        full_text,
        re.IGNORECASE
    )
    if dosage_match:
        dosage = dosage_match.group(1).strip()

    frequency_match = re.search(
        r"(daily|every day|once daily|twice daily|q\.h\.s\.|by mouth daily)",
        full_text,
        re.IGNORECASE
    )
    if frequency_match:
        frequency = frequency_match.group(1).strip()

    refills_match = re.search(r"Refills[:\s]+(\d+)", full_text, re.IGNORECASE)
    if refills_match:
        refills = refills_match.group(1).strip()

    return {
        "Patient Name": patient_name,
        "Date": date,
        "Doctor / Issuer": doctor,
        "Likely Medicine": medicine,
        "Likely Dosage": dosage,
        "Likely Frequency": frequency,
        "Refills": refills
    }