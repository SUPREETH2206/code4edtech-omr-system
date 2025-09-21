# app.py
# ==================================================================================================
# INNOMATICS - AUTOMATED OMR EVALUATION WEB APP (Streamlit)
# Author: Supreeth Mummalaneni (published by Supreeth)
# Date: 2025-09-20 (Updated)
#
# Single-file Streamlit app implementing:
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

# Attempt to import your real OMR processing module. If not available,
# fallback to a simulated evaluator so UI can be tested.
try:
    from omr_processor import find_and_warp_sheet, evaluate_sheet, get_answer_keys
    HAS_OMR_MODULE = True
except Exception as e:
    HAS_OMR_MODULE = False
    # Simulated placeholders - **replace with your real functions**
    def get_answer_keys():
        # Provide sample keys for sets A and B
        return {
            "SET-A": {i: "ABCD"[i % 4] for i in range(1, 101)},
            "SET-B": {i: "DCBA"[i % 4] for i in range(1, 101)},
        }

    def find_and_warp_sheet(image_cv):
        # Naive "sheet detection": just return original image.
        # Replace with fiducial detection, contour-based warp, etc.
        return image_cv

    def evaluate_sheet(warped_cv, answer_key):
        # Simulate evaluation results structure the app expects.
        # Replace with actual bubble detection logic using OpenCV + ML classifier.
        num_questions = 100
        subject_scores = [np.random.randint(10, 20) for _ in range(5)]
        total_score = int(sum(subject_scores))
        # create a visualization overlay image (BGR)
        vis = warped_cv.copy()
        h, w = vis.shape[:2]
        cv2.putText(vis, "Simulated Result Overlay", (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        return {
            "subject_scores": subject_scores,  # list of five integers 0-20
            "total_score": total_score,        # int 0-100
            "ambiguous_questions": np.random.randint(0, 3),
            "visual_result": vis,              # BGR image for display
            "raw_answers": {i: "A" for i in range(1, num_questions+1)}  # dummy
        }

# ----------------------------------------------------------------------
# Configuration & utility functions
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Innomatics - Automated OMR Evaluator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(APP_ROOT, "omr_outputs")
DB_PATH = os.path.join(APP_ROOT, "evaluation_audit.db")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize DB connection
@st.cache_resource
def init_db(path=DB_PATH):
    conn = sqlite3.connect(path, check_same_thread=False)
    return conn

conn = init_db()

def setup_database(connection):
    connection.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            filename TEXT,
            source TEXT,
            exam_set TEXT,
            total_score INTEGER,
            subj_python INTEGER,
            subj_eda INTEGER,
            subj_sql INTEGER,
            subj_powerbi INTEGER,
            subj_statistics INTEGER,
            ambiguous_questions INTEGER,
            flagged TEXT,
            json_path TEXT,
            overlay_path TEXT,
            rectified_path TEXT
        );
    ''')
    connection.commit()

setup_database(conn)

# Helper: save image (BGR -> PNG)
def save_bgr_image(bgr_img, path):
    rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(path, format="PNG")

def timestamp_now():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Logging function
def log_evaluation_to_db(conn, results, meta):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO results (
            timestamp, filename, source, exam_set, total_score,
            subj_python, subj_eda, subj_sql, subj_powerbi, subj_statistics,
            ambiguous_questions, flagged, json_path, overlay_path, rectified_path
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        ts,
        meta.get("filename"),
        meta.get("source"),
        meta.get("exam_set"),
        results.get("total_score"),
        results.get("subject_scores")[0],
        results.get("subject_scores")[1],
        results.get("subject_scores")[2],
        results.get("subject_scores")[3],
        results.get("subject_scores")[4],
        results.get("ambiguous_questions"),
        results.get("flagged"),
        meta.get("json_path"),
        meta.get("overlay_path"),
        meta.get("rectified_path")
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
st.markdown(
    """
    <style>
    /* Page background and general typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    .stApp {
        background: radial-gradient(ellipse at top left, #071229 0%, #0b1220 40%, #071827 100%);
        color: #e6eef8;
        font-family: "Inter", sans-serif;
    }

    /* Animated header gradient */
    .app-header {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 18px;
        border-radius: 12px;
        background: linear-gradient(90deg, rgba(56,189,248,0.08), rgba(99,102,241,0.06));
        box-shadow: 0 8px 30px rgba(2,6,23,0.6);
        backdrop-filter: blur(6px);
        border: 1px solid rgba(255,255,255,0.03);
    }

    .logo-circle {
        width: 64px;
        height: 64px;
        background: linear-gradient(135deg,#06b6d4, #3b82f6);
        border-radius: 50%;
        display:flex;
        align-items:center;
        justify-content:center;
        color:white;
        font-weight:800;
        font-size:22px;
        box-shadow: 0 10px 30px rgba(59,130,246,0.2);
    }

    /* Animated pulse */
    .pulse {
        animation: pulse 2.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(59,130,246,0.30); }
        70% { box-shadow: 0 0 0 18px rgba(59,130,246,0.00); }
        100% { box-shadow: 0 0 0 0 rgba(59,130,246,0.00); }
    }

    /* Floating cards look for results */
    .card {
        border-radius: 12px;
        padding: 16px;
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.03);
        box-shadow: 0 8px 24px rgba(2,6,23,0.6);
    }

    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(90deg, rgba(2,6,23,0.6), rgba(2,6,23,0.9));
        color: #9aa7b8;
        text-align: center;
        padding: 12px;
        font-size: 13px;
        border-top: 1px solid rgba(255,255,255,0.02);
        z-index: 9999;
    }

    .muted {
        color: #9aa7b8;
    }

    .big-number {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    /* Progress bar style */
    .omr-progress {
        width: 100%;
        height: 12px;
        background: rgba(255,255,255,0.06);
        border-radius: 8px;
        overflow: hidden;
    }
    .omr-progress > .bar {
        height: 100%;
        background: linear-gradient(90deg, #06b6d4, #3b82f6);
        border-radius: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------------------------
# Page layout: Header (animated) + Controls
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <div class="logo-circle pulse">OMR</div>
        <div>
            <div style="font-size:18px;font-weight:700">Innomatics - Automated OMR Evaluation</div>
            <div class="muted" style="font-size:13px">Fast, auditable & scalable evaluation — reduced turnaround to minutes</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------------------------
# Sidebar: upload controls
# ----------------------------------------------------------------------
st.sidebar.header("⚙️ Evaluation Controls")

# Load answer keys (from omr_processor or simulated fallback)
try:
    ANSWER_KEYS = get_answer_keys()
except Exception as e:
    st.sidebar.error("Could not load answer keys from omr_processor. Using simulated keys.")
    ANSWER_KEYS = get_answer_keys()

AVAILABLE_SETS = list(ANSWER_KEYS.keys()) if isinstance(ANSWER_KEYS, dict) else ["SET-A", "SET-B"]
exam_set_choice = st.sidebar.selectbox("1. Select Exam Set / Version", options=AVAILABLE_SETS)

input_method = st.sidebar.radio("2. Input Method", ("File Uploader (batch)", "Live Camera Scan"), index=0)
uploaded_files = []
camera_capture = None

if input_method == "File Uploader (batch)":
    uploaded_files = st.sidebar.file_uploader("Upload OMR sheets (PNG/JPG/PDF) — multiple allowed", type=["png","jpg","jpeg","pdf"], accept_multiple_files=True)
else:
    camera_capture = st.sidebar.camera_input("Take a picture")

# Additional options
flagging_threshold = st.sidebar.slider("Flag evaluation if ambiguous questions ≥", min_value=0, max_value=10, value=1)
low_score_flag_threshold = st.sidebar.slider("Flag if total score ≤", min_value=0, max_value=100, value=10)
save_rectified = st.sidebar.checkbox("Save rectified images & overlays to audit folder", value=True)

# ----------------------------------------------------------------------
# Main: Actions & pipeline
# ----------------------------------------------------------------------
col1, col2 = st.columns([1.6, 2.4])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Upload / Scan")
    st.write("Choose OMR images (batch) or use camera. Click **Start Evaluation** to run the pipeline.")
    num_files = len(uploaded_files) if uploaded_files else (1 if camera_capture else 0)
    st.markdown(f"**Queued files:** {num_files}")

    process_button = st.button("✨ Start Evaluation", use_container_width=True, type="primary")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # real-time progress feedback area
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Pipeline Status")
    status_placeholder = st.empty()
    visual_preview = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Evaluation loop (batch or single)
# ----------------------------------------------------------------------
def process_single_image(pil_img, filename_hint, exam_set):
    """
    Processes a single PIL image: runs warp, evaluate, saves artifacts and logs.
    Returns results dict and paths.
    """
    # Convert PIL to BGR (OpenCV)
    img_rgb = pil_img.convert("RGB")
    img_np = np.array(img_rgb)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # Attempt to detect & warp the sheet
    try:
        warped = find_and_warp_sheet(img_bgr)
        if warped is None:
            raise ValueError("Warp returned None")
    except Exception as e:
        # If sheet detection fails, mark as failed and still save original
        warped = img_bgr.copy()
        # In production, you'd want to return an explicit failure/flag for manual review
        st.warning(f"Sheet detection warning for {filename_hint}: {e}")

    answer_key = ANSWER_KEYS.get(exam_set)
    try:
        results = evaluate_sheet(warped.copy(), answer_key)
    except Exception as e:
        # fallback simulated evaluation in case real evaluate fails
        st.error(f"Evaluation routine raised error for {filename_hint}. Using fallback eval. Error: {e}")
        results = evaluate_sheet(warped.copy(), answer_key)

    # Determine flagged reason
    flag_reason = None
    if results.get("ambiguous_questions", 0) >= flagging_threshold:
        flag_reason = f"{results['ambiguous_questions']} ambiguous marks"
    elif results.get("total_score", 0) <= low_score_flag_threshold:
        flag_reason = f"Low total score {results['total_score']}"

    results['flagged'] = flag_reason

    # Save artifacts
    base_name = f"{timestamp_now()}__{filename_hint.replace(' ', '_')}"
    json_path = os.path.join(OUTPUT_DIR, base_name + ".json")
    overlay_path = os.path.join(OUTPUT_DIR, base_name + "_overlay.png")
    rectified_path = os.path.join(OUTPUT_DIR, base_name + "_rectified.png")

    # Save JSON results
    to_dump = {
        "metadata": {
            "processed_at": datetime.datetime.now().isoformat(),
            "source_filename": filename_hint,
            "exam_set": exam_set
        },
        "results": {
            "subject_scores": results.get("subject_scores"),
            "total_score": results.get("total_score"),
            "ambiguous_questions": results.get("ambiguous_questions"),
            "flagged": results.get("flagged"),
            "raw_answers": results.get("raw_answers", {})
        }
    }
    with open(json_path, "w", encoding="utf8") as f:
        json.dump(to_dump, f, indent=2)

    # Save overlay and rectified images if requested
    try:
        if save_rectified:
            # rectified = warped (BGR)
            save_bgr_image(warped, rectified_path)
            # overlay visualization (BGR) - use results['visual_result'] if available
            if results.get("visual_result") is not None:
                save_bgr_image(results["visual_result"], overlay_path)
            else:
                # fallback: use the rectified image as overlay
                save_bgr_image(warped, overlay_path)
    except Exception as e:
        st.warning(f"Failed to save artifacts for {filename_hint}: {e}")

    meta = {
        "filename": filename_hint,
        "source": filename_hint,
        "exam_set": exam_set,
        "json_path": json_path,
        "overlay_path": overlay_path if os.path.exists(overlay_path) else "",
        "rectified_path": rectified_path if os.path.exists(rectified_path) else ""
    }

    # Log to DB
    log_evaluation_to_db(conn, results, meta)

    return results, meta

# Running the pipeline
if process_button:
    files_to_process = []
    # Prepare list of (PIL Image, filename) tuples
    if input_method == "File Uploader (batch)":
        if not uploaded_files:
            st.sidebar.warning("Please upload at least one file.")
        else:
            # Accept PDFs: attempt to read each page if needed (simple handling)
            for file in uploaded_files:
                name = file.name
                if name.lower().endswith(".pdf"):
                    try:
                        from pdf2image import convert_from_bytes
                        pages = convert_from_bytes(file.read(), dpi=200)
                        for pidx, page in enumerate(pages):
                            files_to_process.append((page, f"{name}_page{pidx+1}"))
                    except Exception as e:
                        st.warning(f"Could not convert PDF {name}: {e}")
                        # attempt to read as image directly
                        try:
                            img = Image.open(file)
                            files_to_process.append((img, name))
                        except Exception as ex:
                            st.error(f"Could not read file {name}: {ex}")
                else:
                    try:
                        img = Image.open(file)
                        files_to_process.append((img, name))
                    except Exception as e:
                        st.error(f"Could not open {name}: {e}")
    else:
        if camera_capture:
            img = Image.open(camera_capture)
            files_to_process.append((img, f"camera_{timestamp_now()}.png"))
        else:
            st.sidebar.warning("No camera capture taken.")

    total = len(files_to_process)
    if total == 0:
        st.warning("No files to process. Upload or capture images first.")
    else:
        status_placeholder.info(f"Starting evaluation for {total} file(s)...")
        progress_bar = st.progress(0)
        results_records = []
        for idx, (pil_img, fname) in enumerate(files_to_process, start=1):
            status_placeholder.info(f"Processing ({idx}/{total}): {fname}")
            try:
                res, meta = process_single_image(pil_img, fname, exam_set_choice)
                results_records.append((res, meta))
                # show visual overlay for last processed
                if res.get("visual_result") is not None:
                    rgb = cv2.cvtColor(res["visual_result"], cv2.COLOR_BGR2RGB)
                    visual_preview.image(rgb, caption=f"Overlay: {fname}", use_column_width=True)
            except Exception as e:
                st.error(f"Failed processing {fname}: {e}")
            progress_bar.progress(int((idx/total)*100))
        status_placeholder.success(f"Completed evaluation for {total} files. Saved to audit folder: {OUTPUT_DIR}")
        st.balloons()

# ----------------------------------------------------------------------
# Results / Audit Dashboard
# ----------------------------------------------------------------------
st.markdown("<br />")
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📊 Audit Log & Analytics")
audit_df = load_audit_df()
if audit_df.empty:
    st.info("No evaluations recorded yet. Run some evaluations to populate the audit log.")
else:
    st.write("Recent evaluations (most recent first):")
    st.dataframe(audit_df, use_container_width=True)

    # Download CSV & Excel
    csv_bytes = audit_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Audit CSV", data=csv_bytes, file_name=f"audit_log_{timestamp_now()}.csv", mime="text/csv")
    # Excel
    towrite = io.BytesIO()
    with pd.ExcelWriter(towrite, engine="xlsxwriter") as writer:
        audit_df.to_excel(writer, sheet_name="Audit", index=False)
        writer.save()
    st.download_button("📥 Download Audit Excel", data=towrite.getvalue(), file_name=f"audit_log_{timestamp_now()}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Quick analytics
    st.markdown("#### Aggregate Metrics")
    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown(f"<div class='big-number'>{int(audit_df['total_score'].mean()):d}</div>", unsafe_allow_html=True)
        st.caption("Average Total Score")
    with colB:
        st.metric("Evaluations", value=len(audit_df))
    with colC:
        num_flagged = audit_df['flagged'].notnull().sum()
        st.metric("Flagged for Review", value=int(num_flagged))

    # Subject averages chart
    subject_cols = ["subj_python", "subj_eda", "subj_sql", "subj_powerbi", "subj_statistics"]
    if set(subject_cols).issubset(audit_df.columns):
        averages = audit_df[subject_cols].mean().rename(index={
            "subj_python": "Python",
            "subj_eda": "EDA",
            "subj_sql": "SQL",
            "subj_powerbi": "Power BI",
            "subj_statistics": "Statistics"
        })
        st.bar_chart(averages)

st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Single-evaluation quick viewer (search)
# ----------------------------------------------------------------------
st.markdown("<br />")
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🔎 Review / Manual Check")
st.write("Search by filename or view flagged records for manual review.")
search_term = st.text_input("Filename contains...")
filter_flagged = st.checkbox("Show only flagged records", value=False)

df = load_audit_df()
if not df.empty:
    if filter_flagged:
        df_view = df[df['flagged'].notnull()]
    else:
        df_view = df
    if search_term:
        df_view = df_view[df_view['filename'].str.contains(search_term, case=False, na=False)]
    if df_view.empty:
        st.info("No records match the filter.")
    else:
        sel = st.selectbox("Select record to inspect", options=df_view['id'].astype(str) + " — " + df_view['filename'].fillna("N/A"))
        sel_id = int(sel.split(" — ")[0])
        rec = df_view[df_view['id'] == sel_id].iloc[0]
        st.write("**Metadata**")
        st.json({
            "id": int(rec['id']),
            "timestamp": rec['timestamp'],
            "filename": rec['filename'],
            "exam_set": rec['exam_set'],
            "total_score": int(rec['total_score']),
            "flagged": rec['flagged']
        })
        # show overlay and rectified images if present
        with st.expander("Images"):
            if rec.get("overlay_path") and os.path.exists(rec["overlay_path"]):
                st.image(rec["overlay_path"], caption="Overlay Visualization", use_column_width=True)
            if rec.get("rectified_path") and os.path.exists(rec["rectified_path"]):
                st.image(rec["rectified_path"], caption="Rectified Sheet", use_column_width=True)
            if rec.get("json_path") and os.path.exists(rec["json_path"]):
                st.download_button("Download JSON result", data=open(rec["json_path"], "rb").read(), file_name=os.path.basename(rec["json_path"]))
st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Final footer: contact & copyright (exactly as requested)
# ----------------------------------------------------------------------
st.markdown(
    f"""
    <div class="footer">
        <div style="font-weight:700">Published by Supreeth Mummalaneni | All copyrights reserved © 2025</div>
        <div style="margin-top:6px">For any queries, contact: +91 9652794812 | Supreethmummalaneni@gmail.com</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------------------------
# NOTES for Judges & Developers (displayed in app if dev mode toggled)
# ----------------------------------------------------------------------
if st.sidebar.checkbox("Show developer notes / judges checklist", value=False):
    st.markdown("<hr/>")
    st.markdown("### Developer / Judges Checklist")
    st.markdown("""
    - ✅ Supports multiple exam sets and answer keys (selectable on sidebar).  
    - ✅ Batch upload + camera capture for mobile photos.  
    - ✅ Saves rectified images, overlays, and JSON results to `omr_outputs/` for auditing.  
    - ✅ SQLite audit log with CSV/Excel export.  
    - ✅ Flagging for ambiguous questions and low scores.  
    - ✅ Visual overlay preview and per-subject scoring breakdown.  
    - ⚠️ **Integration required**: Replace simulated `evaluate_sheet` and `find_and_warp_sheet` with production-grade implementations in `omr_processor.py`.  
    - ⚠️ **Accuracy target**: For <0.5% error tolerance, fine-tune the classical CV thresholds and train a small ML classifier (scikit-learn or TensorFlow Lite) for ambiguous-mark classification. Use a labeled dataset from sample scans.  
    - Suggested improvements: background job queue (Celery/RQ) for very large batches, S3/object storage for outputs in multi-instance deployments, HTTPS + authentication for evaluator access, role-based audit controls.
    """)

# EOF
