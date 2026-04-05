# 🏥 AI Healthcare Assistant

A smart healthcare prototype that helps users understand medicine labels and prescriptions using AI-powered cognitive services.

---

## 📌 Features

### 📦 Medicine Label Reader

- Upload medicine label or packaging image
- Extract text using OCR
- Translate text into multiple languages
- Supports Finnish, Urdu, Arabic, French, Spanish

### 📄 Prescription Analyzer

- Upload prescription image
- Extract raw text using OCR
- Parse important fields such as:
  - Patient name
  - Medicine
  - Dosage
  - Frequency
  - Doctor name
  - Refills

---

## 🧠 Technologies Used

- Python
- Streamlit (UI)
- OCR.Space API (Text extraction)
- Deep Translator (Google Translate)
- Regex-based parsing

---

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/talhanayyar98/ai-healthcare-assistant.git
cd ai-healthcare-assistant
```

### 2. Install dependencies

pip install -r requirements.txt

### 3. Create .env file

OCR_SPACE_API_KEY=your_api_key_here

### 4. Run the app

streamlit run app.py

📷 Demo Workflow:
Select feature (Label Reader or Prescription Analyzer)
Upload an image
Click Analyze
View extracted and processed results

🎯 Use Case:
This system helps:

- Patients understand medicine instructions
- Non-native speakers read medical text
- Elderly users with readability issues
- Reduce medication misuse
