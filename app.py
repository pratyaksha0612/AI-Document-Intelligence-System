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

.main {
    background-color: #0E1117;
}

.metric-card {
    background: #1E293B;
    padding: 1rem;
    border-radius: 12px;
}

h1 {
    color: #38BDF8;
}

h2, h3 {
    color: #60A5FA;
}

.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    font-weight: 600;
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

    image = Image.open(uploaded_file)

    image_np = np.array(image)

    if len(image_np.shape) == 3:
        image_cv = cv2.cvtColor(
            image_np,
            cv2.COLOR_RGB2BGR
        )
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