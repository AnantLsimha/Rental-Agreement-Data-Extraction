import streamlit as st
import pandas as pd
from llm_pipeline import process_file

st.set_page_config(page_title="Agreement Metadata Extractor")

st.title(" Agreement Metadata Extractor")

uploaded_file = st.file_uploader(
    "Upload DOCX or PNG agreement",
    type=["docx", "png"]
)

if uploaded_file:
    if st.button("Extract Metadata"):
        with st.spinner("Extracting using AI..."):
            metadata = process_file(uploaded_file)

        st.success("Extraction complete!")

        df = pd.DataFrame(metadata.items(), columns=["Field", "Value"])
        st.table(df)

        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            "metadata.csv",
            "text/csv"
        )
