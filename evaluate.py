import os
import pandas as pd
import streamlit as st
from llm_pipeline import process_file


st.set_page_config(
    page_title="Agreement Metadata Evaluation",
    layout="centered"
)

st.title(" Agreement Metadata Extraction – Evaluation")
st.caption("Strict exact-match recall (LLM-driven correctness only)")

# ---------------- PATH CONFIGURATION ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(BASE_DIR, "test")
TEST_CSV = os.path.join(BASE_DIR, "test.csv")

FIELDS = [
    "agreement_value",
    "agreement_start_date",
    "agreement_end_date",
    "renewal_notice_days",
    "party_one",
    "party_two"
]

CSV_FIELD_MAP = {
    "agreement_value": "Aggrement Value",
    "agreement_start_date": "Aggrement Start Date",
    "agreement_end_date": "Aggrement End Date",
    "renewal_notice_days": "Renewal Notice (Days)",
    "party_one": "Party One",
    "party_two": "Party Two"
}

# ---------------- FILE WRAPPER ----------------
class FileWrapper:
    def __init__(self, f, name):
        self._f = f
        self.name = name

    def __getattr__(self, attr):
        return getattr(self._f, attr)

# ---------------- EVALUATION ----------------
@st.cache_data(show_spinner=True)
def run_evaluation():
    df = pd.read_csv(TEST_CSV)
    stats = {f: {"true": 0, "false": 0} for f in FIELDS}
    outputs = []

    for _, row in df.iterrows():
        base = row["File Name"].lower().strip()
        file_path = None

        for fname in os.listdir(TEST_DIR):
            if fname.lower().startswith(base):
                file_path = os.path.join(TEST_DIR, fname)
                break

        if not file_path:
            continue

        with open(file_path, "rb") as fh:
            wrapped = FileWrapper(fh, os.path.basename(file_path))
            pred = process_file(wrapped)

        outputs.append({
            "file": os.path.basename(file_path),
            "prediction": pred
        })

        for field in FIELDS:
            gt = row[CSV_FIELD_MAP[field]]

            if pd.isna(gt) or str(gt).strip() == "":
                continue

            pr = pred.get(field)

            if str(pr).strip() == str(gt).strip():
                stats[field]["true"] += 1
            else:
                stats[field]["false"] += 1

    recall = {
        f: stats[f]["true"] / (stats[f]["true"] + stats[f]["false"])
        if (stats[f]["true"] + stats[f]["false"]) > 0 else 0.0
        for f in FIELDS
    }

    return recall, outputs

with st.spinner("Evaluating test documents..."):
    recall_scores, outputs = run_evaluation()


st.subheader(" Per-field Recall (Exact Match)")

for field, score in recall_scores.items():
    st.markdown(f"**{field.replace('_', ' ').title()}**")
    st.progress(score)
    st.write(f"Recall: {score:.2f}")
    st.markdown("---")

overall = sum(recall_scores.values()) / len(recall_scores)
st.subheader(" Overall Recall")
st.metric("Average Recall", f"{overall:.2f}")

with st.expander(" Per-document extracted metadata"):
    for item in outputs:
        st.markdown(f"** {item['file']}**")
        st.json(item["prediction"])
        st.markdown("---")
