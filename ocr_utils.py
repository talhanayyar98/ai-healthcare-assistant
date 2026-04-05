import os
import requests
from dotenv import load_dotenv

load_dotenv()

OCR_SPACE_API_KEY = os.getenv("OCR_SPACE_API_KEY")


def extract_text_ocr_space(uploaded_file):
    """
    Extract text from an uploaded image using OCR.Space.
    Returns:
        tuple: (parsed_text, raw_json_response)
    """
    if not OCR_SPACE_API_KEY:
        return "OCR API key not found.", {"error": "Missing OCR_SPACE_API_KEY"}

    url = "https://api.ocr.space/parse/image"

    files = {
        "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
    }

    data = {
        "apikey": OCR_SPACE_API_KEY,
        "language": "eng",
        "isOverlayRequired": False,
        "OCREngine": 2,
        "scale": True
    }

    try:
        response = requests.post(url, files=files, data=data, timeout=60)
        result = response.json()
    except Exception as e:
        return f"Request failed: {str(e)}", {"error": str(e)}

    if result.get("IsErroredOnProcessing"):
        return "OCR processing error.", result

    parsed_results = result.get("ParsedResults", [])
    if parsed_results and parsed_results[0].get("ParsedText"):
        return parsed_results[0]["ParsedText"].strip(), result

    return "No text detected.", result