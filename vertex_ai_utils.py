import json
import os
from typing import Any, Optional

from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
except ImportError:  # pragma: no cover
    genai = None
    types = None

load_dotenv()


def describe_symptom_image(uploaded_file) -> dict[str, Any]:
    if uploaded_file is None:
        return {
            "status": "skipped",
            "provider": "Google Gemini 1.5 Flash via Vertex AI",
            "summary": None,
            "errors": [],
        }

    prompt = (
        "Describe visible health-related findings in this image for a symptom-checker prototype. "
        "Focus on observable issues such as rash, redness, swelling, bruising, wound, cut, or burn. "
        "Keep the description factual, 1 to 3 short sentences, and avoid diagnosis claims."
    )
    text = _call_vertex_with_file(uploaded_file, prompt, os.getenv("VERTEX_IMAGE_MODEL", "gemini-1.5-flash"))
    if text:
        return {
            "status": "ok",
            "provider": "Google Gemini 1.5 Flash via Vertex AI",
            "summary": text.strip(),
            "errors": [],
        }

    return {
        "status": "unavailable",
        "provider": "Google Gemini 1.5 Flash via Vertex AI",
        "summary": None,
        "errors": ["Vertex AI image analysis is not configured or failed."],
    }


def synthesize_final_assessment(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    model = os.getenv("VERTEX_FINAL_MODEL", "gemini-1.5-flash")
    system_prompt = """
You are the final synthesis step in an academic healthcare proof-of-concept.
You receive outputs from three modality-specific providers:
- Azure AI Language Text Analytics for health
- Amazon Transcribe Medical
- Google Gemini via Vertex AI for image understanding

Produce a cautious, non-diagnostic assessment.
If red-flag symptoms are present, recommend urgent medical attention.
Return JSON only with this schema:
{
  "severity": "Mild|Moderate|Severe",
  "urgency": "home_care|monitor|doctor_soon|emergency",
  "possible_conditions": ["..."],
  "recommendation": "...",
  "home_remedies": ["..."],
  "red_flags": ["..."],
  "follow_up": "..."
}
""".strip()
    text = _call_vertex_text(
        system_prompt=system_prompt,
        user_prompt=json.dumps(payload, indent=2),
        model=model,
    )
    return _parse_json_block(text) if text else None


def _call_vertex_text(system_prompt: str, user_prompt: str, model: str) -> Optional[str]:
    client = _get_vertex_client()
    if client is None:
        return None

    try:
        response = client.models.generate_content(
            model=model,
            contents=[
                f"System instruction:\n{system_prompt}",
                f"User request:\n{user_prompt}",
            ],
        )
    except Exception:
        return None

    return getattr(response, "text", None)


def _call_vertex_with_file(uploaded_file, prompt: str, model: str) -> Optional[str]:
    client = _get_vertex_client()
    if client is None or types is None or uploaded_file is None:
        return None

    try:
        response = client.models.generate_content(
            model=model,
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=uploaded_file.getvalue(),
                    mime_type=getattr(uploaded_file, "type", None) or "application/octet-stream",
                ),
            ],
        )
    except Exception:
        return None

    return getattr(response, "text", None)


def _get_vertex_client():
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    if not project or genai is None:
        return None
    try:
        return genai.Client(vertexai=True, project=project, location=location)
    except Exception:
        return None


def _parse_json_block(raw_text: Optional[str]) -> Optional[dict[str, Any]]:
    if not raw_text:
        return None

    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start == -1 or end == -1 or end < start:
        return None

    try:
        return json.loads(raw_text[start : end + 1])
    except json.JSONDecodeError:
        return None
