import streamlit as st
from PIL import Image

from ocr_utils import extract_text_ocr_space
from prescription_parser import parse_prescription_text
from symptom_checker import analyze_symptom_submission
from translate_utils import translate_text_simple

st.set_page_config(page_title="AI Healthcare Assistant", layout="centered")

st.title("AI Healthcare Assistant")
st.write("Choose a feature below and provide the required input.")

with st.sidebar:
    st.subheader("Part 3 Architecture")
    st.write("Text: Azure AI Language Text Analytics for health")
    st.write("Voice: Amazon Transcribe Medical")
    st.write("Image: Google Gemini 1.5 Flash via Vertex AI")
    st.write("Final: Google Gemini 1.5 Flash via Vertex AI")

st.subheader("Select Feature")

mode = st.radio(
    "What would you like to analyze?",
    ["Medicine Label Reader", "Prescription Analyzer", "Symptom Checker"],
    horizontal=True,
)

if mode in {"Medicine Label Reader", "Prescription Analyzer"}:
    target_language = None
    if mode == "Medicine Label Reader":
        target_language = st.selectbox(
            "Translate extracted text to",
            ["Finnish", "Urdu", "Arabic", "French", "Spanish"],
        )

    uploaded_file = st.file_uploader(
        "Upload image",
        type=["png", "jpg", "jpeg"],
        key="ocr_image_upload",
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("Analyze", key="ocr_analyze_button"):
            with st.spinner("Extracting text from image..."):
                extracted_text, _raw_result = extract_text_ocr_space(uploaded_file)

            st.subheader("Extracted Text")
            st.text_area("Original Text", extracted_text, height=200)

            if mode == "Medicine Label Reader":
                with st.spinner("Translating text..."):
                    translated_text = translate_text_simple(extracted_text, target_language)

                st.subheader("Translated Text")
                st.text_area("Translated Text", translated_text, height=200)

            else:
                parsed = parse_prescription_text(extracted_text)

                st.subheader("Parsed Prescription Fields")
                for key, value in parsed.items():
                    st.write(f"**{key}:** {value}")

else:
    symptom_text = st.text_area(
        "Describe symptoms",
        placeholder=(
            "Example: Itchy red rash on my face for two days. Mild burning. "
            "No breathing problem."
        ),
        height=140,
    )

    symptom_image = st.file_uploader(
        "Upload symptom image (optional)",
        type=["png", "jpg", "jpeg"],
        key="symptom_image_upload",
    )
    if symptom_image is not None:
        image = Image.open(symptom_image)
        st.image(image, caption="Symptom Image", use_container_width=True)

    if hasattr(st, "audio_input"):
        symptom_audio = st.audio_input("Record symptom audio (optional)")
    else:
        symptom_audio = None

    uploaded_audio = st.file_uploader(
        "Upload symptom audio (optional)",
        type=["wav", "mp3", "m4a"],
        key="symptom_audio_upload",
    )
    symptom_audio = symptom_audio or uploaded_audio
    if symptom_audio is not None:
        st.audio(symptom_audio.getvalue())

    if st.button("Analyze Symptoms", key="symptom_analyze_button"):
        if not any([symptom_text.strip(), symptom_image, symptom_audio]):
            st.error("Provide at least one of: symptom text, image, or audio.")
        else:
            with st.spinner("Analyzing symptoms..."):
                result = analyze_symptom_submission(
                    text=symptom_text,
                    image_file=symptom_image,
                    audio_file=symptom_audio,
                )

            st.subheader("Assessment")
            st.write(f"**Severity:** {result['severity']}")
            st.write(f"**Urgency:** {result['urgency']}")
            st.write(f"**Recommendation:** {result['recommendation']}")
            st.write(f"**Follow-up:** {result['follow_up']}")

            st.subheader("Possible Conditions")
            for item in result["possible_conditions"]:
                st.write(f"- {item}")

            st.subheader("Home Remedies")
            if result["home_remedies"]:
                for item in result["home_remedies"]:
                    st.write(f"- {item}")
            else:
                st.write("No home-care suggestion for this level of severity.")

            st.subheader("Red Flags")
            if result["red_flags"]:
                for item in result["red_flags"]:
                    st.write(f"- {item}")
            else:
                st.write("No major red flags detected from the provided input.")

            st.subheader("Detected Inputs")
            extracted_signals = result["extracted_signals"]
            st.write(f"**Text input:** {extracted_signals.get('text') or 'Not provided'}")
            st.write(
                f"**Image summary:** "
                f"{extracted_signals.get('image_summary') or 'Not provided'}"
            )
            st.write(
                f"**Audio transcript:** "
                f"{extracted_signals.get('audio_transcript') or 'Not provided'}"
            )

            st.subheader("Cognitive Services Used")
            provider_map = result["provider_map"]
            st.write(f"**Speech-to-text:** {provider_map['speech_to_text']}")
            st.write(f"**Image analysis:** {provider_map['image_analysis']}")
            st.write(f"**Symptom NLP:** {provider_map['symptom_nlp']}")
            st.write(f"**Final synthesis:** {provider_map['final_synthesis']}")

            st.write("**Pipeline summary:** " + ", ".join(result["powered_by"]))
            st.subheader("Provider Details")
            st.json(result["provider_details"])
            st.warning(result["disclaimer"])
