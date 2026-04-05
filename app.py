import streamlit as st
from PIL import Image

from ocr_utils import extract_text_ocr_space
from translate_utils import translate_text_simple
from prescription_parser import parse_prescription_text

st.set_page_config(page_title="AI Healthcare Assistant", layout="centered")

st.title("AI Healthcare Assistant")
st.write("Choose a feature below and upload an image for analysis.")

# Main UI mode selector
st.subheader("Select Feature")

mode = st.radio(
    "What would you like to analyze?",
    ["Medicine Label Reader", "Prescription Analyzer"],
    horizontal=True
)

# Language selection only for label reader
target_language = None
if mode == "Medicine Label Reader":
    target_language = st.selectbox(
        "Translate extracted text to",
        ["Finnish", "Urdu", "Arabic", "French", "Spanish"]
    )

uploaded_file = st.file_uploader(
    "Upload image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Analyze"):
        with st.spinner("Extracting text from image..."):
            extracted_text, raw_result = extract_text_ocr_space(uploaded_file)

        st.subheader("Extracted Text")
        st.text_area("Original Text", extracted_text, height=200)

        if mode == "Medicine Label Reader":
            with st.spinner("Translating text..."):
                translated_text = translate_text_simple(extracted_text, target_language)

            st.subheader("Translated Text")
            st.text_area("Translated Text", translated_text, height=200)

        elif mode == "Prescription Analyzer":
            parsed = parse_prescription_text(extracted_text)

            st.subheader("Parsed Prescription Fields")
            for key, value in parsed.items():
                st.write(f"**{key}:** {value}")