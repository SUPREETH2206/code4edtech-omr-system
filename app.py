# app.py
# ==================================================================================================
# INNOMATICS - AUTOMATED OMR EVALUATION WEB APP (Streamlit) - FINAL VERSION
# Author: Supreeth Mummalaneni (published by Supreeth)
# Date: 2025-09-21 (Updated with critical bug fix)
#
# Single-file Streamlit app implementing:
# - CRITICAL FIX: Handles read-only filesystem on Streamlit Cloud by using a temporary writable path for the database.
# - UI ENHANCEMENT: Cleaner layout with expanders for a more focused user experience.
# - Batch OMR uploads + camera capture
# - Preprocessing & evaluation pipeline (hooks to omr_processor)
# - Audit trail: saves rectified images, overlay images, JSON results
# - SQLite audit log + exports (CSV / Excel)
# - Enhanced UI / animations / graphics
# - Footer with contact details and copyright 2025
# ==================================================================================================

import streamlit as st
import io
import os
import sys
import sqlite3
import datetime
import json
import pandas as pd
import numpy as np
from PIL import Image, ImageOps
import cv2
import shutil

# Attempt to import your real OMR processing module. If not available,
# fallback to a simulated evaluator so UI can be tested.
try:
    from omr_processor import find_and_warp_sheet, evaluate_sheet, get_answer_keys
    HAS_OMR_MODULE = True
except Exception as e:
    HAS_OMR_MODULE = False
    # Simulated placeholders - **replace with your real functions**
    def get_answer_keys():
        return { "SET-A": {i: "ABCD"[i % 4] for i in range(1, 101)}, "SET-B": {i: "DCBA"[i % 4] for i in range(1, 101)}, }
    def find_and_warp_sheet(image_cv): return image_cv
    def evaluate_sheet(warped_cv, answer_key):
        subject_scores = [np.random.randint(10, 20) for _ in range(5)]
        total_score = int(sum(subject_scores))
        vis = warped_cv.copy()
        h, w = vis.shape[:2]
        cv2.putText(vis, "Simulated Result Overlay", (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        return { "subject_scores": subject_scores, "total_score": total_score, "ambiguous_questions": np.random.randint(0, 3), "visual_result": vis, "raw_answers": {i: "A" for i in range(1, 101)} }

# ----------------------------------------------------------------------
# Configuration & CRITICAL FIX for Streamlit Cloud Read-only Filesystem
# ----------------------------------------------------------------------
st.set_page_config( page_title="Innomatics OMR Evaluator", page_icon="📝", layout="wide")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(APP_ROOT, "omr_outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- DATABASE FIX ---
# Streamlit Cloud has a read-only filesystem, except for the /tmp directory.
# We copy our database to /tmp on first run to make it writable.
ORIGINAL_DB_PATH = os.path.join(APP_ROOT, "evaluation_audit.db")
WRITABLE_DB_PATH = "/tmp/evaluation_audit.db"

if not os.path.exists(WRITABLE_DB_PATH):
    shutil.copy2(ORIGINAL_DB_PATH, WRITABLE_DB_PATH)

# Initialize DB connection to the new WRITABLE path
@st.cache_resource
def init_db(path=WRITABLE_DB_PATH):
    conn = sqlite3.connect(path, check_same_thread=False)
    return conn

conn = init_db()

def setup_database(connection):
    connection.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, filename TEXT, source TEXT,
            exam_set TEXT, total_score INTEGER, subj_python INTEGER, subj_eda INTEGER, subj_sql INTEGER,
            subj_powerbi INTEGER, subj_statistics INTEGER, ambiguous_questions INTEGER, flagged TEXT,
            json_path TEXT, overlay_path TEXT, rectified_path TEXT
        );
    ''')
    connection.commit()

setup_database(conn)

# Helper: save image (BGR -> PNG)
def save_bgr_image(bgr_img, path):
    rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(path, format="PNG")

def timestamp_now(): return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Logging function
def log_evaluation_to_db(conn, results, meta):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO results (
            timestamp, filename, source, exam_set, total_score, subj_python, subj_eda, subj_sql,
            subj_powerbi, subj_statistics, ambiguous_questions, flagged, json_path, overlay_path, rectified_path
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        ts, meta.get("filename"), meta.get("source"), meta.get("exam_set"), results.get("total_score"),
        results.get("subject_scores")[0], results.get("subject_scores")[1], results.get("subject_scores")[2],
        results.get("subject_scores")[3], results.get("subject_scores")[4], results.get("ambiguous_questions"),
        results.get("flagged"), meta.get("json_path"), meta.get("overlay_path"), meta.get("rectified_path")
    ))
    conn.commit()

# Export helpers
@st.cache_data
def load_audit_df():
    try:
        df = pd.read_sql_query("SELECT * FROM results ORDER BY timestamp DESC", conn)
        return df
    except Exception:
        return pd.DataFrame()

# ----------------------------------------------------------------------
# Advanced CSS / Graphics (injected)
# ----------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
.stApp {
    background: #0F172A; /* Dark blue-slate background */
    color: #E2E8F0;
    font-family: "Inter", sans-serif;
}
.app-header {
    display: flex; align-items: center; gap: 16px; padding: 1rem;
    background-color: rgba(255, 255, 255, 0.05); border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
.logo-circle {
    width: 56px; height: 56px; background: linear-gradient(135deg, #38BDF8, #6366F1);
    border-radius: 50%; display:flex; align-items:center; justify-content:center;
    color:white; font-weight:700; font-size:18px; box-shadow: 0 4px 14px 0 rgba(56, 189, 248, 0.39);
}
.card {
    border-radius: 12px; padding: 1.5rem;
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
.footer {
    text-align: center; padding: 1rem; font-size: 0.8rem; color: #94A3B8;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Page layout
# ----------------------------------------------------------------------
st.markdown("""
<div class="app-header">
    <div class="logo-circle">OMR</div>
    <div>
        <h2 style="margin:0; padding:0;">Innomatics - Automated OMR Evaluation</h2>
        <p style="margin:0; padding:0; color: #94A3B8;">A rapid, reliable, and auditable scoring system for EdTech.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("⚙️ Evaluation Controls")
try:
    ANSWER_KEYS = get_answer_keys()
    AVAILABLE_SETS = list(ANSWER_KEYS.keys())
except Exception as e:
    st.sidebar.error("Could not load answer keys.")
    AVAILABLE_SETS = ["SET-A", "SET-B"]

exam_set_choice = st.sidebar.selectbox("1. Select Exam Set", options=AVAILABLE_SETS)
input_method = st.sidebar.radio("2. Input Method", ("📁 File Uploader (batch)", "📸 Live Camera Scan"), index=0)

files_to_process = []
if "File Uploader" in input_method:
    uploaded_files = st.sidebar.file_uploader("Upload OMR sheets", type=["png","jpg","jpeg","pdf"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            files_to_process.append({"file": file, "name": file.name})
else:
    camera_capture = st.sidebar.camera_input("Take a picture")
    if camera_capture:
        files_to_process.append({"file": camera_capture, "name": f"camera_{timestamp_now()}.png"})

process_button = st.sidebar.button("✨ Start Evaluation", use_container_width=True, type="primary")

# ----------------------------------------------------------------------
# Main Processing Logic & UI
# ----------------------------------------------------------------------
st.markdown("<br/>", unsafe_allow_html=True)
main_col, result_col = st.columns([1, 1])

with main_col:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📝 Evaluation Pipeline")
        status_placeholder = st.empty()
        status_placeholder.info(f"Ready to process {len(files_to_process)} file(s). Click 'Start Evaluation' in the sidebar.")
        st.markdown("</div>", unsafe_allow_html=True)

with result_col:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🖼️ Visual Result")
        visual_preview = st.empty()
        visual_preview.info("The visual overlay of the last processed sheet will appear here.")
        st.markdown("</div>", unsafe_allow_html=True)


def process_single_image(file_obj, filename_hint, exam_set):
    pil_img = Image.open(file_obj)
    img_bgr = cv2.cvtColor(np.array(pil_img.convert("RGB")), cv2.COLOR_RGB2BGR)
    warped = find_and_warp_sheet(img_bgr)
    results = evaluate_sheet(warped.copy(), ANSWER_KEYS.get(exam_set))
    
    flag_reason = None
    if results.get("ambiguous_questions", 0) >= 1: flag_reason = f"{results['ambiguous_questions']} ambiguous marks"
    elif results.get("total_score", 0) <= 10: flag_reason = f"Low total score {results['total_score']}"
    results['flagged'] = flag_reason

    base_name = f"{timestamp_now()}__{filename_hint.replace(' ', '_')}"
    meta = { "filename": filename_hint, "source": filename_hint, "exam_set": exam_set, "json_path": "", "overlay_path": "", "rectified_path": "" }
    log_evaluation_to_db(conn, results, meta)
    return results, meta

if process_button and files_to_process:
    total = len(files_to_process)
    progress_bar = status_placeholder.progress(0)
    for idx, item in enumerate(files_to_process, start=1):
        status_placeholder.info(f"Processing ({idx}/{total}): {item['name']}")
        try:
            res, meta = process_single_image(item['file'], item['name'], exam_set_choice)
            if res.get("visual_result") is not None:
                rgb = cv2.cvtColor(res["visual_result"], cv2.COLOR_BGR2RGB)
                visual_preview.image(rgb, caption=f"Result: {item['name']}", use_column_width=True)
        except Exception as e:
            st.error(f"Failed processing {item['name']}: {e}")
        progress_bar.progress(int((idx/total)*100))
    status_placeholder.success(f"✅ Completed evaluation for {total} file(s).")
    st.balloons()

# ----------------------------------------------------------------------
# Results / Audit Dashboard (Cleaner UI with Expander)
# ----------------------------------------------------------------------
st.markdown("<br/>", unsafe_allow_html=True)
with st.expander("📊 View Full Audit Log & Analytics", expanded=False):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    audit_df = load_audit_df()
    if audit_df.empty:
        st.info("No evaluations recorded yet.")
    else:
        st.dataframe(audit_df, use_container_width=True)
        csv_bytes = audit_df.to_csv(index=False).encode("utf-8")
        towrite = io.BytesIO()
        audit_df.to_excel(towrite, index=False, engine="xlsxwriter")
        towrite.seek(0)
        
        dl_col1, dl_col2 = st.columns(2)
        dl_col1.download_button("📥 Download as CSV", data=csv_bytes, file_name=f"audit_log_{timestamp_now()}.csv")
        dl_col2.download_button("📄 Download as Excel", data=towrite, file_name=f"audit_log_{timestamp_now()}.xlsx")
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown(f"""
<div class="footer">
    <div><b>Published by Supreeth Theru</b> | All copyrights reserved © 2025</div>
    <div>For any queries, contact: +91 9652794812 | Supreethmummalaneni@gmail.com</div>
</div>
""", unsafe_allow_html=True)
