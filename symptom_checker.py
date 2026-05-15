from aws_transcribe_medical import transcribe_medical_audio
from azure_health_text import analyze_health_text
from severity_rules import build_rule_based_assessment
from vertex_ai_utils import describe_symptom_image, synthesize_final_assessment

DISCLAIMER = (
    "This is an academic proof-of-concept, not a medical diagnosis service. "
    "If symptoms are severe, worsening, or you are unsure, contact a licensed clinician."
)

def analyze_symptom_submission(text="", image_file=None, audio_file=None):
    clean_text = (text or "").strip()
    text_result = analyze_health_text(clean_text) if clean_text else _empty_text_result()
    audio_result = transcribe_medical_audio(audio_file) if audio_file else _empty_audio_result()
    image_result = describe_symptom_image(image_file) if image_file else _empty_image_result()

    final_payload = {
        "user_text_input": clean_text or None,
        "azure_text_result": text_result,
        "aws_audio_result": audio_result,
        "vertex_image_result": image_result,
    }

    combined_text = "\n".join(
        part
        for part in [
            clean_text.strip(),
            audio_result.get("transcript") or "",
            image_result.get("summary") or "",
            text_result.get("summary") or "",
        ]
        if part
    )

    assessment = synthesize_final_assessment(final_payload)
    powered_by = _build_powered_by(text_result, audio_result, image_result, assessment)
    if not assessment:
        assessment = build_rule_based_assessment(combined_text)

    assessment["disclaimer"] = DISCLAIMER
    assessment["extracted_signals"] = {
        "text": clean_text or None,
        "image_summary": image_result.get("summary"),
        "audio_transcript": audio_result.get("transcript"),
    }
    assessment["powered_by"] = powered_by
    assessment["provider_map"] = {
        "speech_to_text": get_speech_provider_name(),
        "image_analysis": get_vision_provider_name(),
        "symptom_nlp": get_nlp_provider_name(),
        "final_synthesis": get_final_provider_name(),
    }
    assessment["provider_details"] = {
        "text_result": text_result,
        "audio_result": audio_result,
        "image_result": image_result,
    }
    return assessment


def get_speech_provider_name() -> str:
    return "Amazon Transcribe Medical"


def get_vision_provider_name() -> str:
    return "Google Gemini 1.5 Flash via Vertex AI"


def get_nlp_provider_name() -> str:
    return "Azure AI Language Text Analytics for health"


def get_final_provider_name() -> str:
    return "Google Gemini 1.5 Flash via Vertex AI"


def _build_powered_by(text_result, audio_result, image_result, final_assessment):
    powered_by = []
    if text_result["status"] == "ok":
        powered_by.append("Azure AI Language Text Analytics for health")
    if audio_result["status"] == "ok":
        powered_by.append("Amazon Transcribe Medical")
    if image_result["status"] == "ok":
        powered_by.append("Google Gemini 1.5 Flash via Vertex AI")
    if final_assessment:
        powered_by.append("Google Gemini 1.5 Flash via Vertex AI")
    else:
        powered_by.append("Local Rule-based Fallback")
    return powered_by


def _empty_text_result():
    return {
        "status": "skipped",
        "provider": get_nlp_provider_name(),
        "summary": None,
        "conditions": [],
        "raw_entities": [],
        "errors": [],
    }


def _empty_audio_result():
    return {
        "status": "skipped",
        "provider": get_speech_provider_name(),
        "transcript": None,
        "job_name": None,
        "errors": [],
    }


def _empty_image_result():
    return {
        "status": "skipped",
        "provider": get_vision_provider_name(),
        "summary": None,
        "errors": [],
    }
