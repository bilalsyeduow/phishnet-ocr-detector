"""
PhishNet – OCR Image Phishing Detector
Streamlit web application.
"""

import streamlit as st
from PIL import Image

from src.pipeline import analyze_image

# Page config
st.set_page_config(
    page_title="PhishNet – OCR Image Phishing Detector",
    page_icon="🎣",
    layout="centered",
)

# Title and subtitle
st.title("PhishNet – OCR Image Phishing Detector")
st.markdown(
    "Upload a screenshot/image. We extract text + URLs and return a phishing risk score with reasons."
)

st.divider()

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image",
    type=["png", "jpg", "jpeg"],
    help="Upload a screenshot or image to analyze for phishing indicators.",
)

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Analyze button
    if st.button("Analyze", type="primary", use_container_width=True):
        with st.spinner("Analyzing image..."):
            result = analyze_image(image)

        st.divider()

        # Risk score display
        score = result["risk_score"]
        label = result["label"]
        confidence = result["confidence"]

        # Color based on label
        if label == "Phishing":
            color = "#ff4b4b"
        elif label == "Suspicious":
            color = "#ffa500"
        else:
            color = "#00c853"

        # Big score display
        st.markdown(
            f"""
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 4rem; font-weight: bold; color: {color};">{score}</div>
                <div style="font-size: 1.5rem; color: {color}; font-weight: 600;">{label}</div>
                <div style="font-size: 1rem; color: gray;">Confidence: {confidence}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # Reasons
        st.subheader("Reasons")
        if result["reasons"]:
            for reason in result["reasons"]:
                st.markdown(f"- {reason}")
        else:
            st.markdown("_No specific indicators detected._")

        # URLs detected
        st.subheader("URLs Detected")
        if result["urls"]:
            for url in result["urls"]:
                st.code(url, language=None)
        else:
            st.markdown("_No URLs found in the image._")

        # Extracted text expanders
        with st.expander("Extracted Text Preview"):
            preview = result["extracted_text_preview"]
            if preview:
                st.text(preview)
            else:
                st.markdown("_No text extracted._")

        with st.expander("Full Extracted Text"):
            full_text = result["extracted_text"]
            if full_text:
                st.text(full_text)
            else:
                st.markdown("_No text extracted._")
