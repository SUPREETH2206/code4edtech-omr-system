# omr_processor.py
# Minimal helper for testing the OMR app

import numpy as np
import cv2

def get_answer_keys():
    keys = {}
    for set_name in ["SET-A", "SET-B"]:
        d = {}
        for i in range(1, 101):
            d[i] = ["A","B","C","D"][(i-1) % 4]
        keys[set_name] = d
    return keys

def find_and_warp_sheet(image_bgr):
    return image_bgr

def evaluate_sheet(warped_bgr, answer_key):
    h, w = warped_bgr.shape[:2]
    rng = np.random.RandomState((h + w) % 100)
    subject_scores = [int(rng.randint(10, 20)) for _ in range(5)]
    total_score = sum(subject_scores)
    ambiguous = int(rng.randint(0, 2))
    vis = warped_bgr.copy()
    cv2.putText(vis, f"Simulated Score: {total_score}/100", (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2, cv2.LINE_AA)
    raw_answers = {i: answer_key.get(i, "A") for i in range(1, 101)}
    return {
        "subject_scores": subject_scores,
        "total_score": total_score,
        "ambiguous_questions": ambiguous,
        "visual_result": vis,
        "raw_answers": raw_answers
    }
