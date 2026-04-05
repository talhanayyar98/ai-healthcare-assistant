from deep_translator import GoogleTranslator


def translate_text_simple(text, target_language):
    """
    Translate text using GoogleTranslator from deep-translator.
    """
    if not text or text.strip() == "":
        return "No text available for translation."

    language_map = {
        "Finnish": "fi",
        "Urdu": "ur",
        "Arabic": "ar",
        "French": "fr",
        "Spanish": "es"
    }
    
    target_code = language_map.get(target_language)

    if not target_code:
        return "Selected language is not supported."

    try:
        translated = GoogleTranslator(source="auto", target=target_code).translate(text)
        return translated
    except Exception as e:
        return f"Translation error: {str(e)}"