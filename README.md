# AI Healthcare Assistant

A multimodal healthcare prototype that helps users understand medicine labels, prescriptions, and symptoms using AI-powered cognitive services.

---

## Features

### Medicine Label Reader
- Upload a medicine label or packaging image
- Extract text using OCR.Space API
- Translate into Finnish, Urdu, Arabic, French, or Spanish

### Prescription Analyzer
- Upload a prescription image
- Extract raw text using OCR
- Parse key fields: Patient Name, Doctor, Medicine, Dosage, Frequency, Date, Refills

### Symptom Checker
- Describe symptoms via text, image, and/or audio
- Text analysis via Azure AI Language Text Analytics for health
- Image analysis via Google Gemini 1.5 Flash (Vertex AI)
- Audio transcription via Amazon Transcribe Medical
- Final synthesis via Google Gemini 1.5 Flash
- Falls back to local rule-based assessment when cloud services are not configured

---

## Technologies

| Layer | Technology |
|---|---|
| UI | Streamlit |
| OCR | OCR.Space API |
| Translation | Deep Translator (Google Translate) |
| Symptom NLP | Azure AI Language Text Analytics for health |
| Speech-to-text | Amazon Transcribe Medical (AWS) |
| Image & Synthesis | Google Gemini 1.5 Flash via Vertex AI |
| Fallback | Local rule-based severity engine |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/talhanayyar98/ai-healthcare-assistant.git
cd ai-healthcare-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Minimum required to run the app (Medicine Label Reader and Prescription Analyzer):

```
OCR_SPACE_API_KEY=your_ocr_space_api_key_here
```

Additional keys to enable Symptom Checker cloud features:

```
# AWS - for audio transcription
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=us-east-1
AWS_TRANSCRIBE_INPUT_BUCKET=your_s3_bucket_name
AWS_TRANSCRIBE_LANGUAGE_CODE=en-US
AWS_TRANSCRIBE_MEDICAL_SPECIALTY=PRIMARYCARE
AWS_TRANSCRIBE_TYPE=DICTATION
AWS_TRANSCRIBE_TIMEOUT_SECONDS=180

# Azure - for symptom text NLP
AZURE_LANGUAGE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_LANGUAGE_KEY=...

# Google Cloud - for image analysis and final synthesis
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
VERTEX_IMAGE_MODEL=gemini-1.5-flash
VERTEX_FINAL_MODEL=gemini-1.5-flash
```

> The Symptom Checker works without cloud credentials using a local rule-based fallback engine.

### 4. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

```
ai-healthcare-assistant/
├── app.py                     # Streamlit UI
├── ocr_utils.py               # OCR.Space text extraction
├── translate_utils.py         # Translation via Deep Translator
├── prescription_parser.py     # Regex-based prescription field parser
├── symptom_checker.py         # Symptom analysis orchestrator
├── aws_transcribe_medical.py  # AWS audio transcription
├── azure_health_text.py       # Azure medical NLP
├── vertex_ai_utils.py         # Gemini image analysis and synthesis
├── severity_rules.py          # Local rule-based fallback
├── provider_config.py         # Provider config helper
├── requirements.txt
├── .env                       # Your credentials (not committed)
└── .env.example               # Credential template
```

---

## Use Cases

- Patients understanding medicine instructions
- Non-native speakers reading medical text
- Checking whether symptoms need urgent care
- Academic demonstration of multimodal cloud AI services

---

> **Disclaimer:** This is an academic proof-of-concept, not a medical diagnosis service. Always consult a licensed clinician for medical advice.
