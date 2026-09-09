import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image

from modules.image_processor import preprocess_image
from modules.ocr_engine import (
    extract_text,
    get_text_data,
    draw_bounding_boxes
)
from modules.confidence_analyzer import calculate_average_confidence
from modules.information_extractor import extract_information
from modules.text_cleaner import clean_ocr_text


st.set_page_config(
    page_title="AI Document Intelligence System",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Outfit:wght@400;600;800&display=swap');

/* Base Styles */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background with gradient */
.stApp {
    background: linear-gradient(135deg, #020617 0%, #0f172a 100%);
    color: #f8fafc;
}

/* Headings with text gradients */
h1 {
    font-family: 'Outfit', sans-serif;
    font-weight: 800 !important;
    background: linear-gradient(90deg, #38BDF8, #818CF8, #C084FC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem !important;
}

h2, h3 {
    font-family: 'Outfit', sans-serif;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
}

/* File Uploader styling */
[data-testid="stFileUploader"] {
    background: rgba(30, 41, 59, 0.4);
    border: 2px dashed rgba(56, 189, 248, 0.4);
    border-radius: 16px;
    padding: 2rem;
    transition: all 0.3s ease;
    backdrop-filter: blur(8px);
}

[data-testid="stFileUploader"]:hover {
    border-color: #38bdf8;
    background: rgba(30, 41, 59, 0.7);
    transform: scale(1.01);
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 1.5rem;
    border-radius: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    backdrop-filter: blur(10px);
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 20px -8px rgba(56, 189, 248, 0.3);
    border-color: rgba(56, 189, 248, 0.4);
}

[data-testid="stMetricLabel"] {
    font-weight: 600;
    color: #94a3b8;
}

[data-testid="stMetricValue"] {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    color: #f8fafc;
}

/* DataFrame / Tables */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.05);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #38BDF8, #818CF8);
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 15px -3px rgba(56, 189, 248, 0.4) !important;
    background: linear-gradient(90deg, #818CF8, #38BDF8) !important;
}

/* Download Button specific targeting */
.stDownloadButton > button {
    background: linear-gradient(90deg, #10b981, #059669);
}

.stDownloadButton > button:hover {
    box-shadow: 0 8px 15px -3px rgba(16, 185, 129, 0.4) !important;
    background: linear-gradient(90deg, #059669, #10b981) !important;
}

/* Text Area */
.stTextArea textarea {
    background-color: rgba(30, 41, 59, 0.6) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    font-family: 'Inter', monospace !important;
}

.stTextArea textarea:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 1px #38bdf8 !important;
}

/* Dividers */
hr {
    border-color: rgba(255, 255, 255, 0.1) !important;
    margin: 2.5rem 0 !important;
}

/* Alerts / Success / Error / Warning Messages */
[data-testid="stAlert"] {
    border-radius: 12px;
    border: none;
    font-weight: 600;
}

/* Hide streamlit default branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #0f172a; 
}
::-webkit-scrollbar-thumb {
    background: #334155; 
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #475569; 
}

/* Image container */
[data-testid="stImage"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: transform 0.3s ease;
}

[data-testid="stImage"]:hover {
    transform: scale(1.02);
}

</style>
""", unsafe_allow_html=True)

st.title("📄 AI Document Intelligence System")
st.caption(
    "AI-Powered OCR, Information Extraction and Document Analysis"
)

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    try:
        image = Image.open(uploaded_file)

        image_np = np.array(image)

        if len(image_np.shape) == 3:
            if image_np.shape[2] == 4:
                image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
            else:
                image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        elif len(image_np.shape) == 2:
            image_cv = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
        else:
            image_cv = image_np

    gray, blurred, threshold = preprocess_image(image_cv)

    text = extract_text(threshold)
    text = clean_ocr_text(text)

    data = get_text_data(threshold)

    confidence = calculate_average_confidence(data)

    info = extract_information(text)

    boxed_image = draw_bounding_boxes(threshold)

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "OCR Confidence",
            f"{confidence}%"
        )

    with col2:
        word_count = len(text.split())
        st.metric(
            "Words Detected",
            word_count
        )
    with col3:
        character_count = len(text)
        st.metric(
            "Characters",
            character_count
        )

    with col4:

        if confidence >= 80:
            st.success("🟢 High Accuracy")

        elif confidence >= 60:
            st.warning("🟡 Medium Accuracy")

        else:
            st.error("🔴 Low Accuracy")

    st.divider()

    st.subheader("Document Processing Pipeline")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Original")
        st.image(
            image,
            use_container_width=True
        )

    with col2:
        st.markdown("### Processed")
        st.image(
            threshold,
            use_container_width=True
        )

    with col3:
        st.markdown("### Detection")
        st.image(
            boxed_image,
            use_container_width=True
        )

    
    st.divider()

    st.subheader("Extracted Information")

    df = pd.DataFrame(
        list(info.items()),
        columns=["Field", "Value"]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("OCR Extracted Text")

    st.text_area(
        "",
        text,
        height=250
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="⬇ Download TXT",
            data=text,
            file_name="ocr_output.txt",
            mime="text/plain"
        )

    with col2:

        csv_data = df.to_csv(
            index=False
        )

        st.download_button(
            label="⬇ Download CSV",
            data=csv_data,
            file_name="extracted_information.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"An error occurred during processing: {str(e)}")
        st.exception(e)