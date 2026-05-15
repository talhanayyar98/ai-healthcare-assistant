from typing import Any

from dotenv import load_dotenv

try:
    from azure.ai.textanalytics import TextAnalyticsClient
    from azure.core.credentials import AzureKeyCredential
except ImportError:  # pragma: no cover
    TextAnalyticsClient = None
    AzureKeyCredential = None

import os

load_dotenv()


def analyze_health_text(text: str) -> dict[str, Any]:
    if not text.strip():
        return {
            "status": "skipped",
            "provider": "Azure AI Language Text Analytics for health",
            "summary": None,
            "conditions": [],
            "raw_entities": [],
            "errors": [],
        }

    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")

    if not endpoint or not key or TextAnalyticsClient is None or AzureKeyCredential is None:
        return {
            "status": "unavailable",
            "provider": "Azure AI Language Text Analytics for health",
            "summary": None,
            "conditions": [],
            "raw_entities": [],
            "errors": ["Azure AI Language credentials or SDK are not configured."],
        }

    try:
        client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        poller = client.begin_analyze_healthcare_entities([text])
        docs = poller.result()
        doc = next(iter(docs), None)
    except Exception as exc:
        return {
            "status": "error",
            "provider": "Azure AI Language Text Analytics for health",
            "summary": None,
            "conditions": [],
            "raw_entities": [],
            "errors": [str(exc)],
        }

    if doc is None or getattr(doc, "is_error", False):
        message = getattr(getattr(doc, "error", None), "message", "Azure analysis failed.")
        return {
            "status": "error",
            "provider": "Azure AI Language Text Analytics for health",
            "summary": None,
            "conditions": [],
            "raw_entities": [],
            "errors": [message],
        }

    conditions = []
    raw_entities = []

    for entity in doc.entities:
        raw_entities.append(
            {
                "text": entity.text,
                "category": entity.category,
                "confidence": entity.confidence_score,
            }
        )
        if entity.category in {"SymptomOrSign", "Diagnosis", "Condition", "ExaminationName"}:
            if entity.text not in conditions:
                conditions.append(entity.text)

    summary = ", ".join(conditions[:5]) if conditions else None
    return {
        "status": "ok",
        "provider": "Azure AI Language Text Analytics for health",
        "summary": summary,
        "conditions": conditions[:5],
        "raw_entities": raw_entities,
        "errors": [],
    }
